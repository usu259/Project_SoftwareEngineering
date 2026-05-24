class DomainError(Exception): pass
class InvalidAttributeValueError(DomainError): pass
class CannotEditError(DomainError): pass
class CannotDeleteError(DomainError): pass
class InvalidStateChangeError(DomainError): pass
class DuplicatePositionError(DomainError): pass
class PositionNotFoundError(DomainError): pass