class CourseStatus:
    ACTIVE = 'active'
    HIDDEN = 'hidden'

class CourseType:
    PUBLIC = 'public'
    PREMIUM = 'premium'

class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

class StudentStatus:
    UNSUBSCRIBED = 'unsubscribed'
    PENDING = 'pending'
    SUBSCRIBED = 'subscribed'

class Regex:
    ACTIVE_HIDDEN = f'^{CourseStatus.ACTIVE}|{CourseStatus.HIDDEN}$'
    PREMIUM_PUBLIC = f'^{CourseType.PREMIUM}|{CourseType.PUBLIC}$'
    UNSUBSCRIBED_SUBSCRIBED = f'^{StudentStatus.UNSUBSCRIBED}|{StudentStatus.PENDING}|{StudentStatus.SUBSCRIBED}$'
