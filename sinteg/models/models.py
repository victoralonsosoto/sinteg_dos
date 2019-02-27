# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
	_inherit = ['res.partner']

	name=fields.Char(track_visibility='onchange')
	street=fields.Char(track_visibility='onchange')
	street2=fields.Char(track_visibility='onchange')
	city=fields.Char(track_visibility='onchange')
	state_id=fields.Many2one(track_visibility='onchange')
	zip=fields.Char(track_visibility='onchange')
	country_id=fields.Many2one(track_visibility='onchange')

	vat=fields.Char(track_visibility='onchange')
	function=fields.Char(track_visibility='onchange')
	phone=fields.Char(track_visibility='onchange')
	mobile=fields.Char(track_visibility='onchange')
	email=fields.Char(track_visibility='onchange')
	website=fields.Char(track_visibility='onchange')
	title=fields.Many2one(track_visibility='onchange')
	lang=fields.Selection(track_visibility='onchange')
	category_id=fields.Many2many(track_visibility='onchange')
	#contacs & address
	#child_id=fields.One2many(track_visibility='onchange')
	#Sales & Purchases
	customer=fields.Boolean(track_visibility='onchange')
	user_id=fields.Many2one(track_visibility='onchange')
	property_delivery_carrier_id=fields.Many2one(track_visibility='onchange')
	message_bounce=fields.Integer(track_visibility='onchange')
	property_payment_term_id=fields.Many2one(track_visibility='onchange')
	ref=fields.Char(track_visibility='onchange')
	barcode=fields.Char(track_visibility='onchange')
	company_id=fields.Many2one(track_visibility='onchange')
	property_stock_customer=fields.Many2one(track_visibility='onchange')
	property_stock_supplier=fields.Many2one(track_visibility='onchange')
	supplier=fields.Boolean(track_visibility='onchange')
	property_supplier_payment_term_id=fields.Many2one(track_visibility='onchange')
	property_account_position_id=fields.Many2one(track_visibility='onchange')

	_sql_constraints = [(
		'default_code_unique',
		'unique(email)',
		'El correo ya existe, favor de modificarlo'
		)]

class Marca(models.Model):
	_name = 'claim.marca'
	name=fields.Char(string='Nombre')



class Modelo(models.Model):
	_name = 'claim.modelo'
	name=fields.Char(string='Nombre')

class claim_picking(models.Model):
	_inherit ='crm.claim.ept'
	picking_id=fields.Many2one('stock.picking' , string='Delivery Order')

	@api.onchange('picking_id')
	def onchange_picking_id(self):
		if self.picking_id:
			self.partner_id = self.picking_id.partner_id.id
			self.partner_phone = self.picking_id.partner_id.phone
			self.email_from = self.picking_id.partner_id.email
			self.sale_id = self.picking_id.sale_id.id
			claim_lines = [
				(0, 0, {'product_id': move.product_id.id,'marca': move.marca.id, 'modelo':move.modelo.id, 'series':move.series,'observaciones':move.observaciones, 'quantity': move.product_uom_qty, 'move_id': move.id}) for
				move in self.picking_id.move_lines]
			self.claim_line_ids = claim_lines

	@api.onchange('partner_id')
	def onchange_partner_id(self):
		if self.partner_id:
			self.partner_phone = self.partner_id.phone
			self.email_from = self.partner_id.email

	# @api.multi
	# def create_tiket(self, amount, commission, type, factura):
	# 	commission_obj = self.env['sales.commission.line']
	# 	product = self.env['product.product'].search([('is_commission_product','=',1)],limit=1)
	# 	for vivienda in self:
	# 		if amount != 0.0:
	# 			commission_value = {
	# 			# 'sales_team_id': invoice.team_id.id,
	# 				'commission_user_id': vivienda.asesor.id,
	# 				'amount': amount,
	# 				'amount_company_currency': amount,
	# 				'origin': vivienda.name,
	# 				'type':type,
	# 				'product_id': product.id,
	# 				'date' : datetime.now(),
	# 				'src_invoice_id': factura,
	# 				'sales_commission_id':commission.id,
	# 			}
	# 			commission_id = commission_obj.create(commission_value)
	# 			if type == 'sales_person':
	# 				vivienda.commission_person_id = commission_id.id
	# 	return True


class claim(models.Model):
	_inherit ='claim.line.ept'
#	equipo = fields.Char(string='Equipo')
	marca = fields.Many2one('claim.marca',string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones')










	

class claim_product(models.Model):
	_inherit ='product.template'
#	equipo = fields.Char(string='Equipo')
	marca = fields.Many2one('claim.marca', string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones')

class claim(models.Model):
	_inherit ='product.product'
	marca = fields.Many2one(related='product_tmpl_id.marca',string='marca')
	modelo = fields.Many2one(related='product_tmpl_id.modelo',string='modelo')

class claim_product(models.Model):
	_inherit ='stock.move'
#	equipo = fields.Char(string='Equipo')
	marca = fields.Many2one('claim.marca', string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	sub_modelo=fields.Many2one('helpdesk.sub_modelo',string='Sub Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones')


class product_product(models.Model):
	_inherit ='product.product'
#	equipo = fields.Char(string='Equipo')
	marca = fields.Many2one('claim.marca', string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones')

# class tipo_contrato(models.Model):
# 	_name = 'helpdesk.tipo.contrato'
# 	name=fields.Char(string='Nombre')

# class equip(models.Model):
# 	_name = 'helpdesk.equipos.contrato'
# 	name=fields.Char(string='Nombre')

class Modelo(models.Model):
	_name = 'helpdesk.sub_modelo'
	name=fields.Char(string='Nombre')


class helpdesk_ticket(models.Model):
	_inherit ='helpdesk.support'

	contrato = fields.Boolean(string='Contrato')
	# equipo_contrato = fields.Many2one('claim.modelo', string='Equipos de Contrato')
	tipo_ticket= fields.Selection(selection=[('CARGO', 'cargo'),('GARANTIA', 'garantia'),
											 ('SERVICIO', 'servicio'),('CONTRATO', 'contrato'),
											 ('INTERNO', 'interno'),('VENTA', 'venta'),
											 ('CALIDAD', 'calidad'),('MAIP', 'ma ip'),
											 ('MAGOB', 'ma gob'),
											 ('SG', 'sg')],string='Tipo de Ticket',default='CARGO')

	tipo= fields.Selection(selection=[('entregar_cli', 'Entregar Cliente'),
									  ('recoleccion_cli', 'Recoleccion Cliente'),
									  ('recoleccion_pro', 'Recoleccion Proveedor'),
									  ('entregar_pro', 'Entregar Proveedor'),
									  ('traslado_per', 'Traslado de Personal'),
									  ('recoger_doc ', 'Recoger Documentos '),
									  ('entregar_doc', 'Entregar Documentos'),
									  ('entrega_rec', 'Entrega y Recoleccion'),
									  ('recoleccion_ent', 'Recoleccion y Entrega')],string='Tipo',default='entregar_cli')

		
	solicitante=fields.Char(string='Solicitante')
	marca = fields.Many2one('claim.marca', string='Marca')
	modelo = fields.Many2one('claim.modelo', string='Modelo')
	series = fields.Char(string='Series')
	observaciones=fields.Text(string='Observaciones Adicionales')
	doc_c = fields.Binary(string='Documento')
	product_id=fields.Many2one('product.product',string='Producto')
	picking_type_id=fields.Many2one('stock.picking.type',string='Tipo de Operación')
	location_dest_id=fields.Many2one('stock.location',string='Ubicación destino')
	location_id = fields.Many2one('stock.location', 'Return Location')
	sub_modelo=fields.Many2one('helpdesk.sub_modelo',string='Sub Modelo')
	falla=fields.Char(string='Falla Reportada')
	des_solicitud=fields.Text(string='Descripción de la Solicitud')
	contacto=fields.Char(string='Contacto')
	descripcion=fields.Text(string='Descripción')
	cantidad=fields.Integer(string='Cantidad')
 
	@api.model
	def _create_apple(self):
		inv_obj = self.env['stock.picking']
		move_line_obj = self.env['stock.move']
		self.ensure_one()		
		cr = self.env.cr
		sql ="select id from helpdesk_support where name='"+str(self.name)+"' limit 1"
		cr.execute(sql)
		id_ticket = cr.fetchone()
		invoice ={
			'partner_id': self.partner_id.id,
			'location_id':self.location_id.id,
			'picking_type_id':self.picking_type_id.id,
			'location_dest_id':self.location_dest_id.id,
			'ticket':id_ticket
		}
		inv_ids = inv_obj.create(invoice)
		inv_id=inv_ids.id
		print(inv_id)
		if inv_id:
			move_line={
			'picking_id':inv_id,
			'name':self.name,
			'product_id':self.product_id.id,
			'marca':  self.marca.id,
			'modelo': self.modelo.id,
			'sub_modelo': self.sub_modelo.id,
			'series': self.series,
			'observaciones': self.observaciones,
			'picking_type_code':'outgoing',
			'product_uom_qty': '0.00',
			'reserved_availability': '0.00',
			'quantity_done':'0.00',
			'product_uom':self.product_id.uom_id.id,
			'product_uom_id':'1',
			'location_id':self.location_id.id,
			'location_dest_id':self.location_dest_id.id
			
			}
			move_ids_without_package=move_line_obj.create(move_line)
		
		return invoice


	def create_apple(self):
		self._create_apple()


	@api.model
	def _create_apple_dos(self):
		inv_obj = self.env['stock.picking']
		move_line_obj = self.env['stock.move']
		self.ensure_one()
		cr = self.env.cr
		sql ="select id from helpdesk_support where name='"+str(self.name)+"' limit 1"
		cr.execute(sql)
		id_ticket = cr.fetchone()
		invoice ={
			'partner_id': self.partner_id.id,
			'location_id':self.location_id.id,
			'picking_type_id':self.picking_type_id.id,
			'location_dest_id':self.location_dest_id.id,			
			'ticket':id_ticket
		}
		inv_ids = inv_obj.create(invoice)
		inv_id=inv_ids.id
		print(inv_id)
		if inv_id:
			move_line={
			'picking_id':inv_id,
			'name':self.name,
			'product_id':self.product_id.id,
			'marca':  self.marca.id,
			'modelo': self.modelo.id,
			'sub_modelo': self.sub_modelo.id,
			'series': self.series,
			'observaciones': self.observaciones,
			'picking_type_code':'incoming',
			'picking_type_id':2,
			'product_uom_qty': '0.00',
			'reserved_availability': '0.00',
			'quantity_done':'0.00',
			'product_uom':self.product_id.uom_id.id,
			'product_uom_id':'1',
			'location_id':self.location_id.id,
			'location_dest_id':self.location_dest_id.id
			
			}
			move_ids_without_package=move_line_obj.create(move_line)
		
		return invoice


	def create_apple_dos(self):
		self._create_apple_dos()
	


class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'


	ticket=fields.Many2one('helpdesk.support',string='Ticket')

class stockpicking(models.Model):
	_inherit = 'stock.picking'


	ticket=fields.Many2one('helpdesk.support',string='Ticket')

