from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):

        if view.basename in ["user"]:
            return bool((request.user.is_authenticated and request.user == obj) or request.user.is_superuser)

        if view.basename in ["order"]:
            return bool(request.user.is_authenticated and request.user == obj.initiator)

        if view.basename in ["product-review"]:
            if request.method in ['POST']:
                return bool(request.user.is_superuser or
                            request.user.products_bought.filter(public_id=obj.public_id).exists()
                            )
            if request.method in ['PATCH']:
                return bool(request.user.is_superuser or request.user == obj.author)

        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        return False

    def has_permission(self, request, view):

        if view.basename in ["product-review"]:
            if request.method in ['DELETE', 'PATCH', 'PUT', 'POST']:
                return request.user.is_authenticated

        if view.basename in ["order"]:
            return bool(request.user.is_authenticated)

        if view.basename in ["user"]:
            return bool(request.user.is_authenticated)

        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        return False
