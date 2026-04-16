"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, bcrypt
from flask import render_template, request, jsonify, send_file, session
from .models import User, Profile, Match, Message, Favorite
from functools import wraps
import os
from werkzeug.utils import secure_filename

# --- Helper Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Login required"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile/<int:id>', methods=['GET'])
@login_required
def get_profile(id):
    profile = Profile.query.get_or_404(id)
    user = User.query.get(profile.user_id)
    
    # Hide if not public and not owner (could also check if matched, but simple for now)
    if not user.is_public and profile.user_id != session['user_id']:
         return jsonify({"error": "This profile is private"}), 403

    profile_data = {
        "id": profile.id,
        "user_id": profile.user_id,
        "name": profile.name,
        "age": profile.age,
        "bio": profile.bio,
        "location": profile.location,
        "interests": profile.interests,
        "profile_pic_url": profile.profile_pic_url,
        "gender": profile.gender,
        "looking_for": profile.looking_for
    }
    return jsonify(profile_data), 200

@app.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    data = request.get_json()

    if not user.profile:
        user.profile = Profile(user_id=user_id, name=data.get('name', 'Anonymous'), age=data.get('age', 18))
        db.session.add(user.profile)
    
    profile = user.profile
    if 'name' in data: profile.name = data['name']
    if 'age' in data: profile.age = data['age']
    if 'bio' in data: profile.bio = data['bio']
    if 'location' in data: profile.location = data['location']
    if 'interests' in data: profile.interests = data['interests']
    if 'gender' in data: profile.gender = data['gender']
    if 'looking_for' in data: profile.looking_for = data['looking_for']
    if 'is_public' in data: user.is_public = data['is_public']

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

@app.route('/profile/photo', methods=['POST'])
@login_required
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo part"}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        # Unique filename using user_id
        user_id = session['user_id']
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        new_filename = f"user_{user_id}_{int(datetime.now().timestamp())}.{ext}"
        
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        file.save(os.path.join(upload_folder, new_filename))
        
        user = User.query.get(user_id)
        if user.profile:
            user.profile.profile_pic_url = new_filename
            db.session.commit()
            return jsonify({"message": "Photo uploaded successfully", "filename": new_filename}), 200
        else:
            return jsonify({"error": "Profile must be created before uploading photo"}), 400

# --- Matching System Endpoints ---

@app.route('/matches', methods=['GET'])
@login_required
def get_matches():
    user_id = session['user_id']
    matches = Match.query.filter(
        ((Match.user1_id == user_id) | (Match.user2_id == user_id)),
        (Match.status == 'matched')
    ).all()
    
    matched_users = []
    for m in matches:
        other_user_id = m.user2_id if m.user1_id == user_id else m.user1_id
        other_user = User.query.get(other_user_id)
        if other_user and other_user.profile:
             matched_users.append({
                 "match_id": m.id,
                 "user_id": other_user_id,
                 "name": other_user.profile.name,
                 "profile_pic_url": other_user.profile.profile_pic_url
             })
             
    return jsonify(matched_users), 200

@app.route('/potential-matches', methods=['GET'])
@login_required
def get_potential_matches():
    user_id = session['user_id']
    user_profile = User.query.get(user_id).profile
    if not user_profile:
        return jsonify({"error": "You must create a profile first"}), 400
    
    # Exclude users already liked/passed/matched
    already_interacted = Match.query.filter((Match.user1_id == user_id)).with_entities(Match.user2_id).all()
    already_interacted_ids = [u[0] for u in already_interacted]
    already_interacted_ids.append(user_id) # exclude self
    
    # Matching algorithm:
    # 1. Base criteria: Same location (if specified) and age within +/- 5 years
    query = Profile.query.filter(~Profile.user_id.in_(already_interacted_ids))
    
    if user_profile.location:
        query = query.filter(Profile.location == user_profile.location)
    
    min_age = user_profile.age - 5
    max_age = user_profile.age + 5
    query = query.filter(Profile.age >= min_age, Profile.age <= max_age)
    
    potential_profiles = query.all()
    
    # 2. Ranking by shared interests
    results = []
    user_interests = set(user_profile.interests or [])
    
    for p in potential_profiles:
        p_interests = set(p.interests or [])
        shared = user_interests.intersection(p_interests)
        
        # 3. Extra criterion: same 'looking_for'
        extra_score = 1 if p.looking_for == user_profile.looking_for else 0
        
        results.append({
            "profile": {
                "id": p.id,
                "user_id": p.user_id,
                "name": p.name,
                "age": p.age,
                "bio": p.bio,
                "location": p.location,
                "profile_pic_url": p.profile_pic_url,
                "interests": p.interests
            },
            "score": len(shared) + extra_score
        })
    
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return jsonify([r['profile'] for r in results]), 200

@app.route('/like/<int:other_user_id>', methods=['POST'])
@login_required
def like_user(other_user_id):
    user_id = session['user_id']
    if user_id == other_user_id:
        return jsonify({"error": "Cannot like yourself"}), 400

    # Check if a like/match already exists from user1 to user2
    existing = Match.query.filter_by(user1_id=user_id, user2_id=other_user_id).first()
    if existing:
        return jsonify({"message": "Already liked/passed this user"}), 200

    # Check if the other user has already liked the current user
    mutual = Match.query.filter_by(user1_id=other_user_id, user2_id=user_id, status='liked').first()
    
    if mutual:
        # Create match record (mutual like)
        mutual.status = 'matched'
        new_match = Match(user1_id=user_id, user2_id=other_user_id, status='matched')
        db.session.add(new_match)
        db.session.commit()
        return jsonify({"message": "It's a match!", "status": "matched"}), 201
    else:
        # Just a like
        new_like = Match(user1_id=user_id, user2_id=other_user_id, status='liked')
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"message": "User liked", "status": "liked"}), 201

@app.route('/pass/<int:other_user_id>', methods=['POST'])
@login_required
def pass_user(other_user_id):
    user_id = session['user_id']
    existing = Match.query.filter_by(user1_id=user_id, user2_id=other_user_id).first()
    if existing:
        return jsonify({"message": "Already interacted"}), 200

    new_pass = Match(user1_id=user_id, user2_id=other_user_id, status='rejected')
    db.session.add(new_pass)
    db.session.commit()
    return jsonify({"message": "User passed"}), 201

# --- Messaging Endpoints ---

@app.route('/messages/<int:match_id>', methods=['GET'])
@login_required
def get_messages(match_id):
    user_id = session['user_id']
    match = Match.query.get_or_404(match_id)
    
    if match.user1_id != user_id and match.user2_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    if match.status != 'matched':
        return jsonify({"error": "Not a mutual match"}), 400

    other_user_id = match.user2_id if match.user1_id == user_id else match.user1_id
    
    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.timestamp.asc()).all()
    
    results = []
    for msg in messages:
        results.append({
            "id": msg.id,
            "sender_id": msg.sender_id,
            "receiver_id": msg.receiver_id,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
            "is_read": msg.is_read
        })
        
        # Mark as read if receiving
        if msg.receiver_id == user_id and not msg.is_read:
            msg.is_read = True
            
    db.session.commit()
    return jsonify(results), 200

@app.route('/messages/<int:match_id>', methods=['POST'])
@login_required
def send_message(match_id):
    user_id = session['user_id']
    match = Match.query.get_or_404(match_id)
    
    if match.user1_id != user_id and match.user2_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    if match.status != 'matched':
        return jsonify({"error": "Not a mutual match"}), 400

    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({"error": "Message content is required"}), 400

    other_user_id = match.user2_id if match.user1_id == user_id else match.user1_id
    
    new_msg = Message(sender_id=user_id, receiver_id=other_user_id, content=content)
    db.session.add(new_msg)
    db.session.commit()
    
    return jsonify({"message": "Message sent", "id": new_msg.id}), 201

@app.route('/conversations', methods=['GET'])
@login_required
def get_conversations():
    user_id = session['user_id']
    # Subquery to get the latest message for each user pair
    # For simplicity, let's just find all matches and get the last message if any
    matches = Match.query.filter(
        ((Match.user1_id == user_id) | (Match.user2_id == user_id)),
        (Match.status == 'matched')
    ).all()
    
    results = []
    for m in matches:
        other_user_id = m.user2_id if m.user1_id == user_id else m.user1_id
        other_user = User.query.get(other_user_id)
        
        last_msg = Message.query.filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
            ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
        ).order_by(Message.timestamp.desc()).first()
        
        results.append({
            "match_id": m.id,
            "other_user": {
                "id": other_user_id,
                "name": other_user.profile.name if other_user.profile else "Unknown",
                "profile_pic_url": other_user.profile.profile_pic_url if other_user.profile else None
            },
            "last_message": {
                "content": last_msg.content if last_msg else None,
                "timestamp": last_msg.timestamp.isoformat() if last_msg else None,
                "is_read": last_msg.is_read if last_msg else True
            }
        })
    
    # Sort by timestamp of last message
    results.sort(key=lambda x: x['last_message']['timestamp'] or "", reverse=True)
    return jsonify(results), 200

# --- Search & Discovery Endpoints ---

@app.route('/search', methods=['GET'])
@login_required
def search_users():
    location = request.args.get('location')
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    interests = request.args.get('interests') # comma separated
    
    query = Profile.query
    
    if location:
        query = query.filter(Profile.location.ilike(f"%{location}%"))
    if min_age:
        query = query.filter(Profile.age >= min_age)
    if max_age:
        query = query.filter(Profile.age <= max_age)
    
    profiles = query.all()
    
    if interests:
        search_interests = [i.strip().lower() for i in interests.split(',')]
        filtered_profiles = []
        for p in profiles:
            p_interests = [i.lower() for i in (p.interests or [])]
            if any(si in p_interests for si in search_interests):
                filtered_profiles.append(p)
        profiles = filtered_profiles

    results = []
    for p in profiles:
        # Check if user is public
        user = User.query.get(p.user_id)
        if user.is_public or p.user_id == session['user_id']:
            results.append({
                "id": p.id,
                "user_id": p.user_id,
                "name": p.name,
                "age": p.age,
                "location": p.location,
                "profile_pic_url": p.profile_pic_url
            })
            
    return jsonify(results), 200

@app.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    user_id = session['user_id']
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    results = []
    for f in favorites:
        fav_user = User.query.get(f.favorite_user_id)
        if fav_user and fav_user.profile:
            results.append({
                "user_id": f.favorite_user_id,
                "name": fav_user.profile.name,
                "profile_pic_url": fav_user.profile.profile_pic_url
            })
            
    return jsonify(results), 200

@app.route('/favorites/<int:fav_user_id>', methods=['POST'])
@login_required
def toggle_favorite(fav_user_id):
    user_id = session['user_id']
    existing = Favorite.query.filter_by(user_id=user_id, favorite_user_id=fav_user_id).first()
    
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({"message": "Removed from favorites"}), 200
    else:
        new_fav = Favorite(user_id=user_id, favorite_user_id=fav_user_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({"message": "Added to favorites"}), 201

# --- End of New Endpoints ---

# --- End of New Endpoints ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful", "user_id": user.id}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200

@app.route('/me', methods=['GET'])
@login_required
def get_me():
    user = User.query.get(session['user_id'])
    profile_data = None
    if user.profile:
        profile_data = {
            "id": user.profile.id,
            "name": user.profile.name,
            "age": user.profile.age,
            "bio": user.profile.bio,
            "location": user.profile.location,
            "interests": user.profile.interests,
            "profile_pic_url": user.profile.profile_pic_url,
            "gender": user.profile.gender,
            "looking_for": user.profile.looking_for
        }
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "profile": profile_data
    }), 200

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return jsonify({"error": "Not Found"}), 404