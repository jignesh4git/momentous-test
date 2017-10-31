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
class DistributerViewSet(viewsets.ModelViewSet):
    queryset = models.Distributer.objects.all()
    serializer_class = data_serializers.DistributerSerializer


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = data_serializers.ProductSerializer

    def get_queryset(self):
        distributor_id = self.request.query_params['id']
        return models.Product.objects.filter(distributer__user_id__exact=distributor_id)


class PlaceOrder(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        # parse data from POST request
        retailer_id = request.user.id
        distributor_id = request.data['distributor_id']
        products = request.data['products']
        quantity = request.data['quantity']

        # fetch retailer and distributor accounts
        retailer = models.Retailer.objects.filter(user_id=retailer_id).first()
        distributor = models.Distributer.objects.filter(user_id=distributor_id).first()

        if retailer is None or distributor is None:
            return Response(status=400, exception=True,
                            data={'error': 'requested retailer or distributor does not exist.'})

        # fetch all products to validate ids
        for item_id in products:
            product = models.Product.objects.filter(id=item_id).first()
            if product is None:
                return Response(status=400, exception=True,
                                data={'error': 'requested product with id ' + str(item_id) + ' does not exist.'})

        # create order object with retailer and distributor
        order = models.Order.objects.create(retailer=retailer,
                                            distributer=distributor,
                                            order_date=datetime.now(),
                                            order_status='REQUESTED_APP')

        # create order items for this order
        for item_id, qty in zip(products, quantity):
            product = models.Product.objects.filter(id=item_id).first()

            models.OrderItem.objects.create(order=order,
                                            product=product,
                                            item_quantity=qty)

        return Response({'status': '200', 'data': request.data})


place_order = PlaceOrder.as_view()
