def _generate_jwt_token(self, user: User) -> str:
    payload = {
        'user_id': user.user_id,
        'username': user.username,
        'role': user.role.value,
        'permissions': [p.value for p in user.permissions],
        'iat': datetime.now(),
        'exp': datetime.now() + timedelta(minutes=self.session_duration_minutes)
    }
    return jwt.encode(payload, self.secret_key, algorithm="HS256")

def validate_token(self, token: str) -> tuple[bool, str, Optional[User]]:
    try:
        payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        
        user_id = payload.get('user_id')
        if not user_id or user_id not in self.users:
            return False, "User not found", None
        
        user = self.users[user_id]
        if not user.is_active:
            return False, "User account is disabled", None
        
        return True, "Token valid", user
        
    except jwt.ExpiredSignatureError:
        return False, "Token has expired", None
    except jwt.InvalidTokenError:
        return False, "Invalid token", None
