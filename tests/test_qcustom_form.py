from qtpy.QtWidgets import QLineEdit


class TestQCustomFormField:
    def test_required_field_reports_error(self, qapp):
        from Custom_Widgets.QCustomForm import QCustomFormField

        field = QCustomFormField("Name")
        field.set_required(True)
        field.set_value("")
        assert field.validate() is False
        assert field.error_text == "Name is required"
        assert field.is_valid is False

    def test_custom_validator_can_succeed(self, qapp):
        from Custom_Widgets.QCustomForm import QCustomFormField

        field = QCustomFormField("Email")
        field.set_validator(lambda value: value.count("@") == 1)
        field.set_value("user@example.com")
        assert field.validate() is True
        assert field.is_valid is True

    def test_value_round_trip(self, qapp):
        from Custom_Widgets.QCustomForm import QCustomFormField

        field = QCustomFormField("Email")
        field.set_value("hello")
        assert field.value() == "hello"


class TestQCustomForm:
    def test_form_validation_collects_errors(self, qapp):
        from Custom_Widgets.QCustomForm import QCustomForm, QCustomFormField

        form = QCustomForm()
        name = QCustomFormField("Name")
        name.set_required(True)
        form.add_field(name)

        email = QCustomFormField("Email")
        email.set_validator(lambda value: "@" in value)
        email.set_value("bad-value")
        form.add_field(email)

        assert form.validate() is False
        assert form.errors()["Name"] == "Name is required"

    def test_submit_emits_signal_when_valid(self, qapp):
        from Custom_Widgets.QCustomForm import QCustomForm, QCustomFormField

        form = QCustomForm()
        name = QCustomFormField("Name")
        name.set_required(True)
        name.set_value("Ada")
        form.add_field(name)

        emitted = []
        form.submitted.connect(lambda payload: emitted.append(payload))
        form.submit()

        assert emitted == [{"Name": "Ada"}]
