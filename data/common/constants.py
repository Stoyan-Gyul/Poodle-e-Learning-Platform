ACTIVE = 'active'
HIDDEN = 'hidden'
PREMIUM = 'premium'
PUBLIC = 'public'

class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

class Status:
    UNSUBSCRIBED = 'unsubscribed'
    PENDING = 'pending'
    SUBSCRIBED = 'subscribed'

class Regex:
    ACTIVE_HIDDEN = f'^{ACTIVE}|{HIDDEN}$'
    PREMIUM_PUBLIC = f'^{PREMIUM}|{PUBLIC}$'
    UNSUBSCRIBED_SUBSCRIBED = '^unsubscribed|pending|subscribed$'
