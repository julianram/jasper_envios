from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _


class jasper_envios(osv.osv):
    _name = 'jasper.envios'
    _description = 'Jasper Envios'
   
    _columns = {
        'name': fields.char('Name', size=128, translate=True, required=True),  # button name
        'enabled': fields.boolean('Active', help="Indicates if this document is active or not"),
        'jasper_id': fields.many2one('jasper.document', 'Documentos Jasper', required=True),  # object model in ir.model
        'query': fields.char('Where consulta', size=1024, required=True, help="Escribir de la forma [('campo','='.condicion)]"),
        'campo': fields.char('Campo', size=1024, required=True, help="Campo para devolver id del partner"),    
        'model_id': fields.many2one('ir.model', 'Object Model', required=True,help="Modelo sobre el que se transfieren los ids para parametro de reporte"),
        'frecuencia': fields.selection([('day', 'Diaria'), ('week', 'Semanal'), ('month', 'Mensual')], 'Frecuencia', select=True,help='Frecuencia del envio del informe'),
        'formato': fields.selection([('pdf', 'PDF'), ('xls', 'Excel'), ('docx', 'Word')], 'Formato', select=True,help='Formato fichero adjunto'),
    }
    
jasper_envios()



