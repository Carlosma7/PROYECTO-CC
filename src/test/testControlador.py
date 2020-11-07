from modelos import *
from typing import List
import pytest
from random import randint
import datetime
import json


class TestController:

	usuarios: List[TestUsuario] = []
	polizas: List[TestPoliza] = []
	prescripciones: List[TestPrescripcion] = []
	
	# [HU1] Creación usuario administrativo
	def crear_admin(self, nombre: str, email: str, dni: str):
		email_empresarial = email.split('@')[0] + '@medauth.com'
		c = TestUsuarioAdmin(nombre, email, dni, email_empresarial)
		len_antes = len(self.usuarios)
		self.usuarios.append(c)
		assert len(self.usuarios) > len_antes
		
		admin = [a for a in self.usuarios if a.get_dni() == dni][0]
		assert admin.get_nombre() == nombre
		assert admin.get_email() == email
		assert admin.get_email_empresarial() == email_empresarial
	
	# [HU2] Creación usuario asegurado
	def crear_cliente(self, nombre: str, email: str, dni: str, cuenta_bancaria: str):
		c = TestUsuarioCliente(nombre, email, dni, cuenta_bancaria, 'a')
		len_antes = len(self.usuarios)
		self.usuarios.append(c)
		assert len(self.usuarios) > len_antes
		
		cliente = [c for c in self.usuarios if c.get_dni() == dni][0]
		assert cliente.get_nombre() == nombre
		assert cliente.get_email() == email
		assert cliente.get_cuenta_bancaria() == cuenta_bancaria
		
	# [HU3] Administrar usuario: Modificación administrador
	def modificar_admin(self, nombre: str, email: str, dni: str):
		admin = [c for c in self.usuarios if c.get_dni() == dni][0]
		assert admin.get_dni() == dni
		
		admin.set_nombre(nombre)
		admin.set_email(email)
		email_empresarial = email.split('@')[0] + '@medauth.com'
		admin.set_email_empresarial(email_empresarial)
		
		assert admin.get_nombre() == nombre
		assert admin.get_email() == email
		assert admin.get_email_empresarial() == email_empresarial
	
	# [HU3] Administrar usuario: Modificación cliente
	def modificar_cliente(self, nombre: str, email: str, dni: str, cuenta_bancaria: str):
		cliente = [c for c in self.usuarios if c.get_dni() == dni][0]
		assert cliente.get_dni() == dni
		
		cliente.set_nombre(nombre)
		cliente.set_email(email)
		cliente.set_cuenta_bancaria(cuenta_bancaria)
		
		assert cliente.get_nombre() == nombre
		assert cliente.get_email() == email
		assert cliente.get_cuenta_bancaria() == cuenta_bancaria
		
	
	# [HU3] Administrar usuario: Eliminar usuario
	def eliminar_usuario(self, dni: str):
		len_antes = len(self.usuarios)
		usuario = [c for c in self.usuarios if c.get_dni() == dni][0]
		self.usuarios.remove(usuario)
		assert len(self.usuarios) < len_antes
	
	# [HU4] Administrar póliza: Crear una póliza
	def crear_poliza(self, dni: str, periodo_carencia: datetime, tipo: str, copagos: float, mensualidad: str, servicios_excluidos: List[str], modulos_extra: List[str]):
		cliente = [c for c in self.usuarios if c.get_dni() == dni][0]
		
		poliza_activa = [p for p in self.polizas if p.get_id_poliza() == cliente.get_id_poliza() and p.get_activa() == True]
		assert len(poliza_activa) == 0
		
		id_poliza = "MA-" + dni[:9]
		polizas_previas = [p for p in self.polizas if p.get_id_poliza()[:12] == id_poliza]
		if len(polizas_previas) > 0:
			id_poliza = id_poliza + str(int(polizas_previas[-1][-1]) + 1)

		polizas = [p for p in self.polizas if p.get_id_poliza() == id_poliza]
		assert len(polizas) == 0
			
		cliente.set_id_poliza(id_poliza)
		assert cliente.get_id_poliza() == id_poliza
		
		p = TestPoliza(cliente, id_poliza, periodo_carencia, tipo, copagos, mensualidad, servicios_excluidos, modulos_extra, True)
		len_antes = len(self.polizas)
		self.polizas.append(p)
		assert len(self.polizas) > len_antes

		poliza = [p for p in self.polizas if p.get_id_poliza() == id_poliza][0]
		assert poliza.get_id_poliza() == id_poliza
		assert poliza.get_periodo_carencia() == periodo_carencia
		assert poliza.get_tipo() == tipo
		assert poliza.get_copagos() == copagos
		assert poliza.get_mensualidad() == mensualidad
		assert poliza.get_servicios_excluidos() == servicios_excluidos
		assert poliza.get_modulos_extra() == modulos_extra
		
	# [HU4] Administrar póliza: Modificar una póliza
	def modificar_poliza(self, dni: str, periodo_carencia: datetime, tipo: str, copagos: float, mensualidad: float, servicios_excluidos: List[str], modulos_extra: List[str]):
		cliente = [c for c in self.usuarios if c.get_dni() == dni][0]
		id_poliza = cliente.get_id_poliza()
		assert cliente.get_dni() == dni
		
		poliza = [p for p in self.polizas if p.get_id_poliza() == id_poliza][0]
		assert poliza.get_id_poliza() == id_poliza
		
		poliza.set_periodo_carencia(periodo_carencia)
		poliza.set_tipo(tipo)
		poliza.set_copagos(copagos)
		poliza.set_mensualidad(mensualidad)
		poliza.set_servicios_excluidos(servicios_excluidos)
		poliza.set_modulos_extra(modulos_extra)
		
		assert poliza.get_periodo_carencia() == periodo_carencia
		assert poliza.get_tipo() == tipo
		assert poliza.get_copagos() == copagos
		assert poliza.get_mensualidad() == mensualidad
		assert poliza.get_servicios_excluidos() == servicios_excluidos
		assert poliza.get_modulos_extra() == modulos_extra
		assert poliza.get_activa() == True
	
	# [HU4] Administrar póliza: Desactivar una póliza
	def desactivar_poliza(self, dni: str):
		cliente = [c for c in self.usuarios if c.get_dni() == dni][0]
		id_poliza = cliente.get_id_poliza()
		poliza = [p for p in self.polizas if p.get_id_poliza() == id_poliza][0]
		assert poliza.get_id_poliza() == cliente.get_id_poliza()
		
		cliente.set_id_poliza("")
		assert cliente.get_id_poliza() == ""
		
		poliza.set_activa(False)
		assert poliza.get_activa() == False
	
	# [HU5] Consultar póliza
	def consultar_poliza(self, dni: str):
		cliente = [c for c in self.usuarios if c.get_dni() == dni][0]
		assert cliente.get_dni() == dni
		
		id_poliza = cliente.get_id_poliza()
		poliza = [p for p in self.polizas if p.get_id_poliza() == id_poliza][0]
		assert poliza.get_id_poliza() == id_poliza
		
		return poliza

	# [HU6] Añadir prescripción médica
	def subir_prescripcion(self, archivo: json):
		return

	# [HU7] Solicitar autorización médica
	def solicitar_autorizacion(self, id_prescripcion: str, asegurado: TestUsuarioCliente):
		return

		
def test_crear_admin():
	t = TestController()
	t.crear_admin("Carlos", "carlos7ma@gmail.com", "75925767-F")
	
def test_crear_cliente():
	t = TestController()
	t.crear_cliente("Juan", "juan@gmail.com", "77925767-Z", "ES12345678")
	
def test_modificar_admin():
	t = TestController()
	t.modificar_admin("Carlos", "terceto@gmail.com", "75925767-F")

def test_modificar_cliente():
	t = TestController()
	t.modificar_cliente("Juan", "juan@gmail.com", "77925767-Z", "ES11223344")

def test_eliminar_usuario():
	t = TestController()
	t.eliminar_usuario("75925767-F")

def test_crear_poliza():
	t = TestController()
	fecha = datetime.datetime(2020, 5, 17)
	t.crear_poliza("77925767-Z", fecha, "Total", 5.99, 50.99, ["TAC", "Apendicitis"], ["Dental"])

def test_modificar_poliza():
	t = TestController()
	fecha = datetime.datetime(2020, 5, 17)
	t.modificar_poliza("77925767-Z", fecha, "Básica", 5.99, 50.99, ["TAC", "Apendicitis"], ["Dental"])

def test_consultar_poliza():
	t = TestController()
	t.consultar_poliza("77925767-Z")
	
def test_desactivar_poliza():
	t = TestController()
	t.desactivar_poliza("77925767-Z")
