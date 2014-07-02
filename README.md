# Jasper Envios 6.1

Este modulo nos permite programar envíos periódicos de los reportes que tengamos alojados en un servidor jasper via email, en los formatos que deseemos.

Se parametriza el where **[('id','=',128)]** señalando los id de los partners a los cuales deseamos enviar el email así como los  días de semana y horas para su envío.

Hay que añadir el siguiente comando en el programador del cron.

## <u>Configuración</u>

	Dependencias externas.

	pip install pyjasperclient

Hay que añadir el siguiente comando en el programador del cron.

host --> Ip del serviror Jasper
dbname --> base de datos openerp

` crontab -e`

    0 22 * * 1,2,3,4,5 python /opt/openerp/infinityloop/jasper_envios/enviarreportes.py -d dbname -u host -f day
    0 22 * * 5 python /opt/openerp/infinityloop/jasper_envios/enviarreportes.py -d dbname -u host -f week

