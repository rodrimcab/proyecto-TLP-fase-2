"""
Suite de Tests para Mini-Parser
Tests unitarios y de integración
"""

import unittest
from mini_parser import MiniParser, AnalizadorLexico, TipoToken, ParserDescendenteRecursivo


class TestAnalizadorLexico(unittest.TestCase):
    """Tests para el analizador léxico"""
    
    def setUp(self):
        self.lexico = AnalizadorLexico()
    
    def test_tokenizacion_basica(self):
        """Test tokenización de oración simple"""
        tokens = self.lexico.tokenizar("el perro come")
        self.assertEqual(len(tokens), 4)  # 3 tokens + FIN
        self.assertEqual(tokens[0].tipo, TipoToken.ARTICULO)
        self.assertEqual(tokens[1].tipo, TipoToken.SUSTANTIVO)
        self.assertEqual(tokens[2].tipo, TipoToken.VERBO)
        self.assertEqual(tokens[3].tipo, TipoToken.FIN)
    
    def test_reconocimiento_articulos(self):
        """Test reconocimiento de artículos"""
        for articulo in ["el", "la", "un", "una", "los", "las"]:
            tokens = self.lexico.tokenizar(articulo)
            self.assertEqual(tokens[0].tipo, TipoToken.ARTICULO)
            self.assertEqual(tokens[0].valor, articulo)
    
    def test_reconocimiento_sustantivos(self):
        """Test reconocimiento de sustantivos"""
        sustantivos = ["perro", "gato", "niño", "casa", "libro"]
        for sustantivo in sustantivos:
            tokens = self.lexico.tokenizar(sustantivo)
            self.assertEqual(tokens[0].tipo, TipoToken.SUSTANTIVO)
    
    def test_reconocimiento_adjetivos(self):
        """Test reconocimiento de adjetivos"""
        adjetivos = ["grande", "pequeño", "rojo", "azul", "hermoso"]
        for adjetivo in adjetivos:
            tokens = self.lexico.tokenizar(adjetivo)
            self.assertEqual(tokens[0].tipo, TipoToken.ADJETIVO)
    
    def test_reconocimiento_verbos(self):
        """Test reconocimiento de verbos"""
        verbos = ["come", "lee", "ve", "quiere", "tiene"]
        for verbo in verbos:
            tokens = self.lexico.tokenizar(verbo)
            self.assertEqual(tokens[0].tipo, TipoToken.VERBO)
    
    def test_palabra_desconocida(self):
        """Test detección de palabras desconocidas"""
        tokens = self.lexico.tokenizar("xyz")
        self.assertEqual(tokens[0].tipo, TipoToken.DESCONOCIDO)
    
    def test_mayusculas_minusculas(self):
        """Test insensibilidad a mayúsculas"""
        tokens1 = self.lexico.tokenizar("El Perro")
        tokens2 = self.lexico.tokenizar("el perro")
        self.assertEqual(tokens1[0].tipo, tokens2[0].tipo)
        self.assertEqual(tokens1[1].tipo, tokens2[1].tipo)


class TestParserDescendenteRecursivo(unittest.TestCase):
    """Tests para el parser"""
    
    def setUp(self):
        self.parser = MiniParser()
    
    def test_oracion_svo_simple(self):
        """Test oración SVO básica"""
        resultado = self.parser.analizar("el perro come un hueso")
        self.assertTrue(resultado["valido"])
    
    def test_oracion_con_adjetivo_sujeto(self):
        """Test oración con adjetivo en sujeto"""
        resultado = self.parser.analizar("el perro grande come un hueso")
        self.assertTrue(resultado["valido"])
    
    def test_oracion_con_adjetivo_complemento(self):
        """Test oración con adjetivo en complemento"""
        resultado = self.parser.analizar("el perro come un hueso grande")
        self.assertTrue(resultado["valido"])
    
    def test_oracion_con_adjetivos_ambos(self):
        """Test oración con adjetivos en sujeto y complemento"""
        resultado = self.parser.analizar("el perro grande come un hueso pequeño")
        self.assertTrue(resultado["valido"])
    
    def test_sin_predicado(self):
        """Test oración sin predicado (inválida)"""
        resultado = self.parser.analizar("el perro grande")
        self.assertFalse(resultado["valido"])
        self.assertEqual(resultado["fase"], "sintáctico")
    
    def test_sin_sujeto(self):
        """Test oración sin sujeto (inválida)"""
        resultado = self.parser.analizar("come un libro")
        self.assertFalse(resultado["valido"])
        self.assertEqual(resultado["fase"], "sintáctico")
    
    def test_orden_incorrecto(self):
        """Test orden de palabras incorrecto"""
        resultado = self.parser.analizar("perro el come libro")
        self.assertFalse(resultado["valido"])
    
    def test_falta_articulo(self):
        """Test falta artículo obligatorio"""
        resultado = self.parser.analizar("el perro come libro")
        self.assertFalse(resultado["valido"])
        self.assertEqual(resultado["fase"], "sintáctico")
    
    def test_palabra_fuera_vocabulario(self):
        """Test palabra fuera de vocabulario"""
        resultado = self.parser.analizar("el perro come una pizza")
        self.assertFalse(resultado["valido"])
        self.assertEqual(resultado["fase"], "léxico")
    
    def test_multiples_articulos(self):
        """Test variación de artículos"""
        articulos = ["el", "la", "un", "una", "los", "las"]
        for art1 in articulos[:3]:
            for art2 in articulos[:3]:
                oracion = f"{art1} perro come {art2} libro"
                resultado = self.parser.analizar(oracion)
                # Debe ser válido independientemente del artículo usado
                self.assertTrue(resultado["valido"], f"Falló con: {oracion}")


class TestIntegracion(unittest.TestCase):
    """Tests de integración completos"""
    
    def setUp(self):
        self.parser = MiniParser()
    
    def test_conjunto_oraciones_validas(self):
        """Test conjunto de oraciones válidas"""
        oraciones_validas = [
            "el perro come un hueso",
            "la niña lee el libro",
            "un gato grande ve la casa",
            "el niño pequeño quiere un libro rojo",
            "una computadora nueva tiene el carro",
            "los perros buscan las casas",
            "la niña hermosa lee un libro viejo",
        ]
        
        for oracion in oraciones_validas:
            with self.subTest(oracion=oracion):
                resultado = self.parser.analizar(oracion)
                self.assertTrue(resultado["valido"], 
                              f"Falló validación de: {oracion}")
    
    def test_conjunto_oraciones_invalidas(self):
        """Test conjunto de oraciones inválidas"""
        oraciones_invalidas = [
            "el perro grande",  # Sin predicado
            "come el libro",  # Sin sujeto
            "el grande perro come libro",  # Sin artículo en complemento
            "perro el come un libro",  # Orden incorrecto
            "el perro muy grande come el libro",  # "muy" no en vocabulario
            "python es genial",  # Todo fuera de vocabulario
        ]
        
        for oracion in oraciones_invalidas:
            with self.subTest(oracion=oracion):
                resultado = self.parser.analizar(oracion)
                self.assertFalse(resultado["valido"],
                               f"No detectó error en: {oracion}")
    
    def test_casos_limite(self):
        """Test casos límite"""
        # Oración más corta posible válida
        resultado = self.parser.analizar("el perro come un libro")
        self.assertTrue(resultado["valido"])
        
        # Oración con máximo de adjetivos permitidos
        resultado = self.parser.analizar("el perro grande come un hueso pequeño")
        self.assertTrue(resultado["valido"])
        
        # String vacío
        resultado = self.parser.analizar("")
        self.assertFalse(resultado["valido"])
    
    def test_rendimiento(self):
        """Test básico de rendimiento"""
        import time
        
        oracion = "el niño pequeño quiere un libro rojo"
        inicio = time.time()
        
        for _ in range(1000):
            self.parser.analizar(oracion)
        
        tiempo_total = time.time() - inicio
        tiempo_promedio = tiempo_total / 1000
        
        # Debe procesar 1000 oraciones en menos de 1 segundo
        self.assertLess(tiempo_total, 1.0,
                       f"Demasiado lento: {tiempo_promedio*1000:.3f}ms por oración")


class TestErrores(unittest.TestCase):
    """Tests de manejo de errores"""
    
    def setUp(self):
        self.parser = MiniParser()
    
    def test_mensaje_error_lexico(self):
        """Test mensajes de error léxico"""
        resultado = self.parser.analizar("el perro come pizza")
        self.assertFalse(resultado["valido"])
        self.assertEqual(resultado["fase"], "léxico")
        self.assertIn("pizza", str(resultado["errores"]))
    
    def test_mensaje_error_sintactico(self):
        """Test mensajes de error sintáctico"""
        resultado = self.parser.analizar("el perro grande")
        self.assertFalse(resultado["valido"])
        self.assertEqual(resultado["fase"], "sintáctico")
        self.assertTrue(len(resultado["errores"]) > 0)
    
    def test_multiples_errores_lexicos(self):
        """Test múltiples errores léxicos"""
        resultado = self.parser.analizar("python es genial")
        self.assertFalse(resultado["valido"])
        self.assertEqual(resultado["fase"], "léxico")
        # Debe reportar 3 palabras desconocidas
        self.assertEqual(len(resultado["errores"]), 3)


def ejecutar_suite_completa():
    """Ejecuta todos los tests y genera reporte"""
    print("="*70)
    print("SUITE DE TESTS - MINI-PARSER")
    print("="*70)
    print()
    
    # Crear suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestAnalizadorLexico))
    suite.addTests(loader.loadTestsFromTestCase(TestParserDescendenteRecursivo))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    suite.addTests(loader.loadTestsFromTestCase(TestErrores))
    
    # Ejecutar con verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Reporte final
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    print(f"Tests ejecutados: {resultado.testsRun}")
    print(f"Tests exitosos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Tests fallidos: {len(resultado.failures)}")
    print(f"Errores: {len(resultado.errors)}")
    
    if resultado.wasSuccessful():
        print("\n✓ TODOS LOS TESTS PASARON")
    else:
        print("\n✗ ALGUNOS TESTS FALLARON")
    
    print("="*70)
    
    return resultado.wasSuccessful()


if __name__ == "__main__":
    import sys
    exito = ejecutar_suite_completa()
    sys.exit(0 if exito else 1)
