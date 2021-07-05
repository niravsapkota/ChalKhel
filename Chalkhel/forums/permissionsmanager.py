from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            owner = obj.owner
        except Exception as e:
            try:
                owner = obj.user
            except Exception as e:
                try:
                    owner = obj.member
                except Exception as e:
                    raise e
        # Instance must have an attribute named `owner`.
        return owner == request.user


class SufficientPrestigeOrCantCreate(permissions.BasePermission):
    """
    Object-level permission to only allow authenticated users with more than X prestige to create new forum.
    """

    def has_permission(self, request, view):
        threshold = 0
        if request.method == 'POST':
            return request.user.profiles.prestige_points >= threshold

        return True

class IsReceiverOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow receivers of notifications to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            owner = obj.receiving_user
        except Exception as e:
            raise e
        # Instance must have an attribute named `owner`.
        return owner == request.user