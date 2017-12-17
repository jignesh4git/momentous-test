# Create your views here.

from partner import models
from . import data_serializers
from datetime import datetime

from rest_framework import viewsets
from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = data_serializers.UserSerializer


# ViewSets define the view behavior.
class DistributorViewSet(viewsets.ModelViewSet):
    queryset = models.Distributor.objects.all()
    serializer_class = data_serializers.PartnerAccountSerializer


# ViewSets define the view behavior.
class ManufacturerViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        m_cp = models.ConnectedPartner.objects.filter(connected_partner__user=user, partner__type='manufacturer')
        list_m_cp = list(m_cp)
        partner_user = []
        for manufacturer in list_m_cp:
            partner_user.append(manufacturer.partner.user)

        partners = models.Partner.objects.filter(user__in=partner_user)
        return partners

    serializer_class = data_serializers.PartnerAccountSerializer


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = data_serializers.ProductSerializer

    def get_queryset(self):
        user = self.request.user
        seller_id = self.request.query_params['id']
        products = models.Product.objects.filter(connected_partner__user=user, partner__user__id=seller_id,
                                                 is_active=True)
        return products


class MyProductsView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        user = request.user

        if type(user).__name__ == 'AnonymousUser':
            return Response(status=400, exception=True,
                            data={'error': 'Auth token is missing.'})

        products = models.Product.objects.filter(connected_partner__user=user)
        products_data = data_serializers.ProductSerializer(products, many=True).data
        return Response({'status': '200', 'data': products_data})


class PlaceOrder(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        # parse data from POST request

        requester_id = request.user.id
        products = request.data['products']
        quantity = request.data['quantity']

        # fetch all products to validate ids
        for item_id in products:
            product = models.Product.objects.filter(id=item_id).first()
            if product is None:
                return Response(status=400, exception=True,
                                data={'error': 'requested product with id ' + str(item_id) + ' does not exist.'})

            placed_to_user_id = request.data['place_order_to']

            placed_to = models.Partner.objects.filter(user_id=placed_to_user_id).first()
            placed_by = models.Partner.objects.filter(user_id=requester_id).first()

            order = models.Order.objects.create(partner=placed_by,
                                                connected_partner=placed_to,
                                                order_date=datetime.now(),
                                                delivery_date=datetime.now(),
                                                requested_delivery_time=datetime.now(),
                                                order_status='REQUESTED_APP')

        # create order items for this order
        for item_id, qty in zip(products, quantity):
            product = models.Product.objects.filter(id=item_id).first()

            models.OrderItem.objects.create(order=order,
                                            product=product,
                                            item_quantity=qty)

        return Response({'status': '200', 'data': request.data})


class AccountView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        user = request.user

        if type(user).__name__ == 'AnonymousUser':
            return Response(status=400, exception=True,
                            data={'error': 'Auth token is missing.'})

        # fetch partner accounts
        partner = models.Partner.objects.filter(user=user).first()

        partner_data = data_serializers.PartnerAccountSerializer(partner).data
        return Response({'status': '200', 'data': partner_data, 'type': partner.type})


class ConnectedRetailerView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        user = request.user

        if type(user).__name__ == 'AnonymousUser':
            return Response(status=400, exception=True,
                            data={'error': 'Auth token is missing.'})

        # fetch connected retailers for this distributor
        my_cp = models.ConnectedPartner.objects.filter(partner__user=user)
        list_my_cp = list(my_cp)
        retailers = []
        for retailer in list_my_cp:
            retailers.append(retailer.connected_partner.user)

        partners = models.Partner.objects.filter(user__in=retailers)
        retailer_data = data_serializers.PartnerAccountSerializer(partners, many=True).data

        return Response({'status': '200', 'data': retailer_data})


class MyOrdersView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        user = request.user

        if type(user).__name__ == 'AnonymousUser':
            return Response(status=400, exception=True,
                            data={'error': 'Auth token is missing.'})

        # fetch retailer or distributor accounts
        retailer = models.Retailer.objects.filter(user=user).first()
        distributor = models.Distributor.objects.filter(user=user).first()

        user_type = 'unknown'

        if retailer is not None and distributor is None:
            user_type = 'retailer'
        else:
            if retailer is None and distributor is not None:
                user_type = 'distributor'

        if user_type == 'unknown':
            return Response(status=400, exception=True,
                            data={'error': 'This account is not a retailer or distributor.'})

        if user_type == 'distributor':
            my_orders = models.Order.objects.filter(distributor=distributor)
            orders_data = data_serializers.OrderSerializer(my_orders, many=True).data
            return Response({'status': '200', 'data': orders_data})

        if user_type == 'retailer':
            my_orders = models.Order.objects.filter(retailer=retailer)
            orders_data = data_serializers.OrderSerializer(my_orders, many=True).data
            return Response({'status': '200', 'data': orders_data})


class MyOrderDetailView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        user = request.user

        if type(user).__name__ == 'AnonymousUser':
            return Response(status=400, exception=True,
                            data={'error': 'Auth token is missing.'})

        # fetch retailer or distributor accounts
        retailer = models.Retailer.objects.filter(user=user).first()
        distributor = models.Distributor.objects.filter(user=user).first()

        user_type = 'unknown'

        if retailer is not None and distributor is None:
            user_type = 'retailer'
        else:
            if retailer is None and distributor is not None:
                user_type = 'distributor'

        if user_type == 'unknown':
            return Response(status=400, exception=True,
                            data={'error': 'This account is not a retailer or distributor.'})

        req_order_id = request.query_params['id']

        order_items = models.OrderItem.objects.filter(order_id=req_order_id)
        orders_data = data_serializers.OrderItemSerializer(order_items, many=True).data
        return Response({'status': '200', 'data': orders_data})


class MyInvoicesView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        user = request.user

        if type(user).__name__ == 'AnonymousUser':
            return Response(status=400, exception=True,
                            data={'error': 'Auth token is missing.'})

        # fetch retailer or distributor accounts
        retailer = models.Retailer.objects.filter(user=user).first()
        distributor = models.Distributor.objects.filter(user=user).first()

        user_type = 'unknown'

        if retailer is not None and distributor is None:
            user_type = 'retailer'
        else:
            if retailer is None and distributor is not None:
                user_type = 'distributor'

        if user_type == 'unknown':
            return Response(status=400, exception=True,
                            data={'error': 'This account is not a retailer or distributor.'})

        if user_type == 'distributor':
            connected_retailers = models.Retailer.objects.filter(distributor=distributor)

            response_data = []
            for retailer in connected_retailers:
                retailer_orders = models.Order.objects.filter(distributor=distributor, retailer=retailer)
                orders_data = data_serializers.OrderSerializer(retailer_orders, many=True).data
                response_data.append({"retailer_id": retailer.id, "orders": orders_data})

            return Response({'status': '200', 'data': response_data})

        if user_type == 'retailer':
            my_orders = models.Order.objects.filter(retailer=retailer)
            orders_data = data_serializers.OrderSerializer(my_orders, many=True).data
            return Response({'status': '200', 'data': orders_data})


place_order = PlaceOrder.as_view()
get_account = AccountView.as_view()
get_connected_retailers = ConnectedRetailerView.as_view()
get_my_products = MyProductsView.as_view()
get_orders = MyOrdersView.as_view()
get_order_detail = MyOrderDetailView.as_view()
get_invoices = MyInvoicesView.as_view()
