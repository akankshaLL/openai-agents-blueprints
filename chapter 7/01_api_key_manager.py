class APIKeyManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.keys: Dict[str, APIKeyInfo] = {}
        self.usage_tracking: Dict[str, UsageMetrics] = {}
        self.security_events: List[SecurityEvent] = []
        self.rate_limits: Dict[str, List[float]] = {}
    
    def create_key(
        self,
        name: str,
        description: str,
        scope: KeyScope = KeyScope.READ_ONLY,
        expires_in_days: Optional[int] = None,
        allowed_tools: Optional[List[str]] = None,
        rate_limit: int = 1000,
        ip_whitelist: Optional[List[str]] = None
    ) -> tuple[str, str]:
        key_id = self._generate_key_id()
        
        # Create key info with comprehensive metadata
        key_info = APIKeyInfo(
            key_id=key_id,
            key_hash=self._hash_key(api_key),
            name=name,
            description=description,
            scope=scope,
            status=KeyStatus.ACTIVE,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=expires_in_days) if expires_in_days else None,
            allowed_tools=allowed_tools or [],
            rate_limit=rate_limit,
            ip_whitelist=ip_whitelist or []
        )
        
        self.keys[key_id] = key_info
        self.usage_tracking[key_id] = UsageMetrics()
        
        # Log security event for key creation
        self._log_security_event(
            "key_created",
            key_id=key_id,
            details={
                "name": name,
                "scope": scope.value,
                "rate_limit": rate_limit
            }
        )
        
        return key_id, api_key
