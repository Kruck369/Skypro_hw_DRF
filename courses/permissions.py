from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object().owner


class CoursesPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action == 'create':
            return request.user.is_authenticated
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj == view.obj.owner or request.user.is_staff
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_staff
        elif view.action == 'destroy':
            return request.user == obj.owner
        else:
            return False
