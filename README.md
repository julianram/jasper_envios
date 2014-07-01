# Jasper Envios 6.1

Este modulo nos permite programar envíos periódicos via email, en los formatos que deseemos, de los reportes que tengamos alojados en JasperServer, es perfectamente configurable desde OpenErp.

Se seleccionan los partners que deseamos que reciban la información , ademas de días de semana y horas.

Hay que añadir el siguiente comando en el programador del cron.

## <u>Configuración</u>

	Dependencias externas.

	pip install pyjasperclient

`host --> Ip del serviror Jasper
dbname --> base de datos openerp
`

    0 22 * * 1,2,3,4,5 python /opt/openerp/infinityloop/jasper_envios/enviarreportes.py -d dbname -u host -f day
    0 22 * * 5 python /opt/openerp/infinityloop/jasper_envios/enviarreportes.py -d dbname -u host -f week

