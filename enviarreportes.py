# -*- coding: iso-8859-1 -*-
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import xmlrpclib
import sys, getopt
import datetime
from pyjasperclient import JasperClient


class envioReporte:
    
    
    def __init__(self,dbname,host_url_jasper,frecuencia):
        """Incializa conexión al servidor openerp , asignar el usuario y contraseña"""
        self.dbname=dbname
        user        = 'XXXXX'
        self.pwd    = 'XXXXX'
        self.frecuencia = frecuencia
        host_url    ='localhost'
        sock        = xmlrpclib.ServerProxy('http://%s:8069/xmlrpc/common' % host_url)
        self.uid    = sock.login(dbname,user,self.pwd)
        self.sock   = xmlrpclib.ServerProxy('http://%s:8069/xmlrpc/object' % host_url)
        self.host_jasper = "http://%s:8080/jasperserver/services/repository?wsdl" % host_url_jasper
    
    def sendmail(self,mensaje,subject,desde,to,replyto,file,filename):
        loginmail="XXXXX"
        passwordmail ="XXXXX"
        msg = MIMEMultipart()
        msg['Subject'] =subject
        msg['From'] = desde
        msg['Reply-to'] = replyto
        msg['To'] = to
        msg.preamble = 'Multipart massage.\n' 
        part = MIMEText(mensaje,'html')
        msg.attach(part)
        part = MIMEApplication(file)
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)
        smtp = SMTP("infinityloop.es",25)
        smtp.ehlo()
        smtp.starttls()
        smtp.login("info@infinityloop.es", "casiopea1966")
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp.close()


    def llamareporte(self,nombre,camino,par_id,formato):
        USER_JASPER   = ""
        PASSWD_JASPER = ""
        j = JasperClient(camino,USER_JASPER,PASSWD_JASPER)
        ret = j.runReport(nombre,formato,params={"OERP_ID": '%s' % par_id})
        return ret['data']


    def buscadirEnvio(self,id):
        args=[('partner_id','=',id)]
        ids_dire       = self.sock.execute(self.dbname,self.uid,self.pwd,'res.partner.address','search',args)
        if ids_dire:
            dire_vals  = self.sock.execute(self.dbname,self.uid,self.pwd,'res.partner.address','read',ids_dire,['email'])
        else:
            dire_vals = []
            
        return dire_vals
       


    def generaReportes(self):
        avisolegal="""
        <b>AVISO LEGAL</b>
        <p>
        <p>
        <p>La información incluida en el presente es SECRETO PROFESIONAL Y CONFIDENCIAL, siendo para el uso exclusivo del destinatario de correo arriba mencionado. Si usted lee este mensaje y no es el destinatario seï¿½alado, el empleado o el agente responsable de entregar el mensaje al destinatario, o ha recibido esta comunicación por error, le informamos que está totalmente prohibida su divulgación o reproducción de esta comunicación y le rogamos que lo notifique inmediatamente y nos devuelva el mensaje original a la direcciï¿½n arriba mencionada y borre el mensaje. Gracias</p>
        <p>
        <p>
        <p>The information contained in this e-mail is LEGALLY PRIVILEDGED AND CONFIDENTIAL, and is intended only for the use of the addressee named above. If the reader of this message is not the intended recipiente or the employee or agent responsible for delivering the message to the intended recipiente, or you have recived this communication is strictly prohibited, and please notify us immediately and returm the original message to us at the address above. Thank you</p>
        """
        de='administracion@infinityloop.es'
        report_name ='/openerp/bases/%s/' % self.dbname
        #('date','>=',datetime.datetime.now().strftime('%d-%m-%Y'))
        #Reportes a enviar.
        args=[('enabled','=',True),('frecuencia','=',self.frecuencia),]
        ids_envios  = self.sock.execute(self.dbname,self.uid,self.pwd,'jasper.envios','search',args)
        if ids_envios:
            envios_vals       = self.sock.execute(self.dbname,self.uid,self.pwd,'jasper.envios','read',ids_envios,['jasper_id','model_id','query','name','formato','campo'])
            for envios in envios_vals:
                reports_vals      = self.sock.execute(self.dbname,self.uid,self.pwd,'jasper.document','read',envios['jasper_id'][0],['report_unit','model_id'])
                reporte= report_name+reports_vals['report_unit']
                #Buscamos por el model id para parametrizar por fechas y obtener los ids de ese dia.
                model_vals = self.sock.execute(self.dbname,self.uid,self.pwd,'ir.model','read',envios['model_id'][0],['model'])
                ids_objs   = self.sock.execute(self.dbname,self.uid,self.pwd,model_vals['model'],'search',eval(envios['query']))
                if ids_objs:
                    for pid in ids_objs:
                        objs_vals = self.sock.execute(self.dbname,self.uid,self.pwd,model_vals['model'],'read',pid,[envios['campo']]) 
                        if len(objs_vals)==1:
                            val_part = objs_vals.get(envios['campo'])
                        else:
                            val_part = objs_vals.get(envios['campo'])[0]
                        dire_vals = self.buscadirEnvio(val_part)                  
                        data = self.llamareporte(reporte ,self.host_jasper,pid,envios['formato'])
                        if dire_vals and len(data)!=0:
                            for emails in dire_vals:
                                email= emails['email']
                                if email:
                                    self.sendmail( avisolegal,'%s correspondiente al dï¿½a %s '% ( envios['name'],datetime.datetime.now() ) ,de, email, None, data, 'envios_%s.%s' % (ids_objs[0], envios['formato']) )

  
 
def main(argv):
   print argv
   dbname="XXXXX"
   host_url_jasper="XXXXX"
   try:
    opts, args = getopt.getopt(argv,"hd:u:f:",["dbname=","urljasper=","frecuencia="])
   except getopt.GetoptError:
      print 'enviareportes.py -d <dbname> -u <urljasper> -f <day,week,month>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'enviareportes.py -d <dbname> -u <urljasper> -f <day,week,month>'
         sys.exit()
      elif opt in ("-d", "--ddbname"):
         dbname = arg
      elif opt in ("-u", "--uurljasper"):
         host_url_jasper = arg
      elif opt in ("-f", "--ffrecuencia"):
         frecuencia = arg
   reporte= envioReporte(dbname,host_url_jasper,frecuencia) 
   reporte.generaReportes()                 


if __name__ == "__main__":
    main(sys.argv[1:])
