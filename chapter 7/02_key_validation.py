def validate_key(
    self,
    api_key: str,
    required_scope: Optional[KeyScope] = None,
    required_tools: Optional[List[str]] = None,
    client_ip: Optional[str] = None
) -> tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    if not self._validate_key_format(api_key):
        self._log_security_event(
            "invalid_key_format",
            details={"attempted_key_prefix": api_key[:10]}
        )
        return False, "Invalid key format", None
    
    key_hash = self._hash_key(api_key)
    key_info = self._find_key_by_hash(key_hash)
    
    if not key_info:
        self._log_security_event(
            "unknown_key_used",
            details={"key_hash": key_hash[:16]}
        )
        return False, "Invalid API key", None
    
    # Comprehensive validation checks
    if key_info.status != KeyStatus.ACTIVE:
        return False, f"Key is {key_info.status.value}", None
    
    if key_info.expires_at and datetime.now() > key_info.expires_at:
        self._update_key_status(key_info.key_id, KeyStatus.EXPIRED)
        return False, "Key has expired", None
    
    # IP whitelist validation
    if key_info.ip_whitelist and client_ip:
        if client_ip not in key_info.ip_whitelist:
            self._log_security_event(
                "unauthorized_ip",
                key_id=key_info.key_id,
                ip_address=client_ip,
                severity="warning"
            )
            return False, "IP address not authorized", None
    
    # Rate limiting check
    if not self._check_rate_limit(key_info.key_id, key_info.rate_limit):
        return False, "Rate limit exceeded", None
    
    # Scope permission validation
    if required_scope and not self._check_scope_permission(key_info.scope, required_scope):
        return False, "Insufficient permissions", None
    
    # Tool-specific permission validation
    if required_tools:
        missing_tools = set(required_tools) - set(key_info.allowed_tools)
        if missing_tools and key_info.allowed_tools:
            return False, f"Tool access denied: {missing_tools}", None
    
    # Update usage metrics
    self._update_usage_metrics(key_info.key_id)
    
    return True, None, {
        "key_id": key_info.key_id,
        "scope": key_info.scope.value,
        "allowed_tools": key_info.allowed_tools,
        "name": key_info.name
    }
