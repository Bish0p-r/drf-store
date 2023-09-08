from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ["user"]:
            return bool(request.user.is_authenticated and request.user == obj or request.user.is_superuser)

        if view.basename in ["order"]:
            return bool(request.user.is_authenticated and request.user == obj.initiator)

        if view.basename in ["product-review"]:
            return bool(request.user.is_authenticated and request.user == obj.author)

        return False

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ["product-review"]:
            if request.method in ['DELETE', 'PATCH', 'PUT', 'POST']:
                product_id = request.parser_context["kwargs"]["product_public_id"]
                return bool(request.user.is_superuser
                            or request.user.products_bought.filter(public_id=product_id).exists())
            else:
                return request.method in SAFE_METHODS

        if view.basename in ["order"]:
            return bool(request.user.is_authenticated)

        return False
