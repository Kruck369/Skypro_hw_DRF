from rest_framework.permissions import BasePermission

from courses.models import Subscription


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class IsModeratorOrIsOwner(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        return request.user == view.get_object().owner


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object().owner


class CoursesPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action in ['create', 'subscribe']:
            return request.user
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        elif view.action == 'unsubscribe':
            return request.user
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj == obj.owner or request.user.is_staff
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_staff
        elif view.action == 'destroy':
            return request.user == obj.owner
        elif view.action in 'subscribe':
            return request.user
        elif view.action in 'unsubscribe':
            return request.user
        else:
            return False
