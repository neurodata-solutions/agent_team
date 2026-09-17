"""Testes de contrato para hhmmss.seconds_to_hhmmss.

Escritos a partir apenas dos criterios de aceitacao da TASK-20260915-002,
sem leitura previa da implementacao (piloto de convergencia independente).

Contrato: modulo `hhmmss.py`, funcao `seconds_to_hhmmss(seconds) -> str`.
"""

import unittest

import hhmmss


class TestContratoModulo(unittest.TestCase):
    """O modulo deve expor a funcao com o nome exato do contrato."""

    def test_funcao_existe(self):
        self.assertTrue(
            hasattr(hhmmss, "seconds_to_hhmmss"),
            "modulo hhmmss nao expoe seconds_to_hhmmss",
        )

    def test_funcao_e_chamavel(self):
        self.assertTrue(callable(hhmmss.seconds_to_hhmmss))

    def test_retorna_str(self):
        self.assertIsInstance(hhmmss.seconds_to_hhmmss(0), str)


class TestValoresDeAceitacao(unittest.TestCase):
    """Casos literais listados nos criterios de aceitacao."""

    def test_zero(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(0), "00:00:00")

    def test_sessenta_e_um(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(61), "00:01:01")

    def test_uma_hora_um_minuto_um_segundo(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(3661), "01:01:01")

    def test_vinte_e_quatro_horas(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(86400), "24:00:00")


class TestHorasSemModulo24(unittest.TestCase):
    """Horas podem passar de 23 e de dois digitos; nunca aplicar modulo 24."""

    def test_cem_horas(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(100 * 3600), "100:00:00")

    def test_cem_horas_com_resto(self):
        self.assertEqual(
            hhmmss.seconds_to_hhmmss(100 * 3600 + 2 * 60 + 3), "100:02:03"
        )

    def test_mil_horas(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(1000 * 3600), "1000:00:00")

    def test_vinte_e_cinco_horas(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(90000), "25:00:00")


class TestFormatacaoEPreenchimento(unittest.TestCase):
    """Zero-padding de duas casas e limites de carry."""

    def test_um_segundo(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(1), "00:00:01")

    def test_cinquenta_e_nove_segundos(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(59), "00:00:59")

    def test_sessenta_segundos_vira_um_minuto(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(60), "00:01:00")

    def test_3599_segundos(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(3599), "00:59:59")

    def test_3600_segundos(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(3600), "01:00:00")

    def test_86399_segundos(self):
        self.assertEqual(hhmmss.seconds_to_hhmmss(86399), "23:59:59")

    def test_formato_tem_tres_campos(self):
        partes = hhmmss.seconds_to_hhmmss(45296).split(":")
        self.assertEqual(len(partes), 3)
        self.assertEqual(partes, ["12", "34", "56"])

    def test_minutos_e_segundos_sempre_duas_casas(self):
        for segundos in (0, 5, 61, 3661, 86400, 360000):
            with self.subTest(segundos=segundos):
                horas, minutos, segs = hhmmss.seconds_to_hhmmss(segundos).split(":")
                self.assertEqual(len(minutos), 2, "minutos devem ter 2 digitos")
                self.assertEqual(len(segs), 2, "segundos devem ter 2 digitos")
                self.assertGreaterEqual(len(horas), 2, "horas devem ter >= 2 digitos")


class TestNegativosGeramValueError(unittest.TestCase):
    """Inteiros negativos: ValueError."""

    def test_menos_um(self):
        with self.assertRaises(ValueError):
            hhmmss.seconds_to_hhmmss(-1)

    def test_menos_sessenta_e_um(self):
        with self.assertRaises(ValueError):
            hhmmss.seconds_to_hhmmss(-61)

    def test_negativo_grande(self):
        with self.assertRaises(ValueError):
            hhmmss.seconds_to_hhmmss(-86400)


class TestTiposInvalidosGeramTypeError(unittest.TestCase):
    """str, float, bool e None: TypeError (bool antes de int por subclasse)."""

    def test_str(self):
        with self.assertRaises(TypeError):
            hhmmss.seconds_to_hhmmss("61")

    def test_str_nao_numerica(self):
        with self.assertRaises(TypeError):
            hhmmss.seconds_to_hhmmss("abc")

    def test_float(self):
        with self.assertRaises(TypeError):
            hhmmss.seconds_to_hhmmss(61.0)

    def test_float_fracionario(self):
        with self.assertRaises(TypeError):
            hhmmss.seconds_to_hhmmss(61.5)

    def test_bool_true(self):
        with self.assertRaises(TypeError):
            hhmmss.seconds_to_hhmmss(True)

    def test_bool_false(self):
        with self.assertRaises(TypeError):
            hhmmss.seconds_to_hhmmss(False)

    def test_none(self):
        with self.assertRaises(TypeError):
            hhmmss.seconds_to_hhmmss(None)

    def test_float_negativo(self):
        """Float negativo deve gerar TypeError (tipo verificado antes de valor)."""
        with self.assertRaises(TypeError):
            hhmmss.seconds_to_hhmmss(-1.0)


if __name__ == "__main__":
    unittest.main()
