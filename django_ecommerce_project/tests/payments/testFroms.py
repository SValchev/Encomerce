
class FormTestrMixin():
    def assertFormatError(self,form_cls,exptected_error_name,exptected_error_message,data):
        form = form_cls(data=data)
        from pprint import pformat
        
        
        self.assertFalse(form.isvalid())
        self.assertEquals(
            form.errors[exptected_error_name],
            exptected_error_message,
            msg = "Expected {} : Actual {} : using data {}".format(form.errors[exptected_error_message],exptected_error_message, pformat(data))            )

