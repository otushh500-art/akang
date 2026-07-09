# Backend events (from app/websocket/events.py)
backend_events = {
    # Drops
    "drop_created", "drop_feed_init", "live_drop", "top_win", "recent_drop",
    # Notifications
    "notification",
    # System
    "system_message", "ping", "pong", "connected", "error", "subscribed",
    # Battle Step 13A
    "battle_state", "battle_round", "battle_end", "battle_countdown",
    "battle_joined", "battle_created", "battle_started",
    "round_started", "round_result", "battle_finished",
    "bot_joined", "bot_removed",
    # Battle Step 13B
    "spectator_joined", "spectator_left", "battle_synced",
    "battle_reconnected", "battle_cancelled", "leader_changed",
    "recovery_mode_changed", "bot_profile_changed",
    # Provably Fair
    "provably_fair_rotated", "provably_fair_verified",
    # Economy
    "economy_updated", "recovery_mode_enabled", "recovery_mode_disabled",
    "economy_alert", "whale_detected", "rtp_changed",
    # Payment Hardening
    "payment_received", "withdraw_requested", "withdraw_approved",
    "withdraw_rejected", "payment_alert", "payment_frozen",
    # Admin
    "asset_uploaded", "asset_deleted", "asset_updated",
    "skin_updated", "case_updated", "admin_alert",
    "user_banned", "market_updated",
    # Creator + User Control
    "creator_updated", "creator_earnings_updated", "referral_registered",
    "promo_activated", "user_restricted", "session_revoked",
    "risk_score_updated", "creator_payout_updated",
    # Security
    "security_alert", "user_shadow_banned", "lockdown_enabled",
    "lockdown_disabled", "session_compromised", "websocket_rate_limited",
    "integrity_violation",
    # Premium Battle
    "premium_battle_denied",
    # Referral Quality
    "referral_confirmed", "referral_reward_granted",
    "referral_pending", "referral_rejected",
    # Telegram Bot
    "telegram_linked", "telegram_notification", "premium_activated",
    "broadcast_sent",
    # Local Payment
    "payment_created", "payment_submitted", "payment_approved",
    "payment_rejected", "payment_expired", "payment_recheck_required",
    "card_limit_reached", "card_disabled",
}

# Frontend events (from cs-case/src/lib/ws/channels.ts)
frontend_events = {
    # System
    "ping", "pong", "connected", "disconnected",
    # Drops
    "drop_created", "live_drop", "top_win", "recent_drop",
    # Battles
    "battle_created", "battle_state", "battle_round",
    "battle_countdown", "battle_synced", "battle_reconnected",
    "round_started", "round_result", "battle_finished",
    "spectator_joined", "spectator_left", "leader_changed",
    "bot_joined", "bot_removed", "battle_cancelled",
    "player_joined", "player_left",
    # Notifications
    "notification", "broadcast_sent", "telegram_notification",
    # Payments
    "payment_received", "payment_created", "payment_submitted",
    "payment_approved", "payment_rejected", "payment_expired",
    # Withdrawals
    "withdrawal_created", "withdrawal_submitted",
    "withdrawal_approved", "withdrawal_rejected",
    # Provably Fair
    "provably_fair_rotated", "provably_fair_verified",
    # Referrals
    "referral_registered", "referral_confirmed", "referral_reward_granted",
    # Creator
    "creator_updated", "creator_earnings_updated", "creator_payout_updated",
    # Admin / Economy
    "admin_alert", "user_banned", "market_updated",
    "economy_updated", "recovery_mode_enabled", "recovery_mode_disabled",
    "security_alert", "lockdown_enabled", "lockdown_disabled",
    "user_restricted", "session_revoked", "risk_score_updated",
    "maintenance_mode_enabled", "maintenance_mode_disabled",
    # Balance / Inventory
    "balance_updated", "balance_pending_updated",
    "inventory_item_added", "inventory_item_removed",
    "inventory_updated", "item_traded",
    # Upgrade
    "upgrade_started", "upgrade_completed", "upgrade_failed",
    "contract_created",
    # User / Session
    "user_online", "user_offline", "user_updated",
    "session_expired", "token_refreshed", "settings_updated",
    # Battle Pass
    "battle_pass_level_up", "battle_pass_reward_claimed", "battle_pass_expired",
    # Promo / Bonus
    "promo_activated", "bonus_granted", "daily_bonus_claimed",
    "free_case_available",
}

# Frontendda backendda yo'q bo'lgan eventlar (frontendda ixtiro qilingan)
frontend_only = frontend_events - backend_events
# Backendda bor, frontendda yo'q
backend_only = backend_events - frontend_events

print("=" * 60)
print(f"Backend total: {len(backend_events)}")
print(f"Frontend total: {len(frontend_events)}")
print(f"Backend-only (MISSING from frontend): {len(backend_only)}")
print(f"Frontend-only (extra/not in backend): {len(frontend_only)}")
print("=" * 60)

if backend_only:
    print("\n❌ BACKEND EVENTS MISSING FROM FRONTEND:")
    for e in sorted(backend_only):
        print(f"   - {e}")
else:
    print("\n✅ All backend events covered in frontend!")

if frontend_only:
    print("\n⚠️  FRONTEND EVENTS NOT IN BACKEND (frontend-invented):")
    for e in sorted(frontend_only):
        print(f"   - {e}")

print()
