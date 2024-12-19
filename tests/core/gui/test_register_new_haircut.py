from barbershop.gui.haircut_registration import register_new_haircut


def test_register_new_haircut():
    register_new_haircut(
        label_income="test",
        label_total_haircuts="test",
        entry_cliente="test",
        entry_corte="Test",
        entry_precio="Test",
        calendar="Test",
        text_registros="Test",
    )

    assert True


def test_register_new_haircut_with_no_prize():
    register = register_new_haircut(
        label_income="test",
        label_total_haircuts="test",
        entry_cliente="test",
        entry_corte="Test",
        entry_precio="Test",
        calendar="Test",
        text_registros="Test",
    )

    assert not register
