from unittest import TestCase
from commons.views import CustomGenericAPIView
from commons.exceptions import GenericServiceError


class Test(TestCase):

    def test_define_view_without_service_class_should_raise_exception(self):

        class ViewTest(CustomGenericAPIView):
            def get_op(self, *args, **kwargs):
                return self.service.get_all()

        test_view = ViewTest()
        self.assertRaises(GenericServiceError, test_view.get_op)
