# -*- coding: utf-8 -*-
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta
import locale

from odoo import tools
from odoo import api, fields, models


class AgenciesReport(models.Model):
    _name = "agencies.report"
    _description = "Agencies Analysis"
    _auto = False

    partner_id = fields.Many2one('res.partner', 'Contract')
    amount_invoiced = fields.Float('Amount Invoiced')
    amount_remaining = fields.Float('Amount Remaining')
    amount_consumed = fields.Float('Amount Consumed')
    month_1 = fields.Float('Month 1')
    month_2 = fields.Float('Month 2')
    month_3 = fields.Float('Month 3')
    month_4 = fields.Float('Month 4')
    month_5 = fields.Float('Month 5')
    month_6 = fields.Float('Month 6')
    month_7 = fields.Float('Month 7')
    month_8 = fields.Float('Month 8')
    month_9 = fields.Float('Month 9')
    month_10 = fields.Float('Month 10')
    month_11 = fields.Float('Month 11')
    month_12 = fields.Float('Month 12')
    further = fields.Float('Further')
    agency_id = fields.Many2one('agency.agency', 'Agency')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        select_ = """
            min(p.id) as id,
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_1,
            
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '1' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '1' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_2,
            
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '2' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '2' month), 'YY') AS INT) 
            THEN sa.amount ELSE 0 END) as month_3,
            
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '3' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '3' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_4,
            
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '4' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '4' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_5,
            
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '5' month), 'MM') AS INT) AND 
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '5' month), 'YY') AS INT) 
            THEN sa.amount ELSE 0 END) as month_6,
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '6' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '6' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_7,
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '7' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '7' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_8,
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '8' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '8' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_9,
            SUM(
            CASE WHEN
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '9' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '9' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_10,
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '10' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '10' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_11,
            SUM(
            CASE WHEN 
            cast(to_char(date_trunc('month', sa.expected_date), 'MM') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '11' month), 'MM') AS INT) AND
            cast(to_char(date_trunc('month', sa.expected_date), 'YY') AS INT) = 
            cast(to_char(date_trunc('month', CURRENT_DATE + interval '11' month), 'YY') AS INT)
            THEN sa.amount ELSE 0 END) as month_12,
            SUM(
            CASE WHEN
            sa.expected_date >=  CURRENT_DATE + interval '12' month
            THEN sa.amount ELSE 0 END) as further,
            SUM(sa.amount) as amount_invoiced,
            SUM(CASE WHEN sa.expected_date < date_trunc('month', CURRENT_DATE) THEN sa.amount ELSE 0 END) as amount_consumed,
            SUM(sa.amount) - SUM(CASE WHEN sa.expected_date < date_trunc('month', CURRENT_DATE) THEN sa.amount ELSE 0 END
            ) as amount_remaining,
            p.partner_id as partner_id,
            s.agency_id as agency_id,
            s.id as sale_order_id
        """

        for field in fields.values():
            select_ += field

        from_ = """
                sale_order s
                      join project_project p on (
                        s.project_id = p.id
                      )
                      join sale_split_amount sa on (
                        s.id = sa.order_id
                      )
                %s
        """ % from_clause

        groupby_ = """
            p.id, s.agency_id, p.partner_id ,  s.id %s
        """ % (groupby)

        return """
        %s (SELECT %s FROM %s WHERE s.agency_id IS NOT NULL AND
         NOT (s.state = ANY(ARRAY['draft', 'sent', 'cancel'])) GROUP BY %s )""" % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        print ('*////////')
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

    @api.model
    def fields_view_get(self, view_id=None, view_type='pivot', toolbar=False, submenu=False):
        res = super(AgenciesReport, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'pivot':
            doc = etree.XML(res['arch'])
            month_1 = self.get_month(0)
            month_2 = self.get_month(1)
            month_3 = self.get_month(2)
            month_4 = self.get_month(3)
            month_5 = self.get_month(4)
            month_6 = self.get_month(5)
            month_7 = self.get_month(6)
            month_8 = self.get_month(7)
            month_9 = self.get_month(8)
            month_10 = self.get_month(9)
            month_11 = self.get_month(10)
            month_12 = self.get_month(11)
            for node in doc.xpath("//field[@name='month_1']"):
                node.set('string', month_1)
            for node in doc.xpath("//field[@name='month_2']"):
                node.set('string', month_2)
            for node in doc.xpath("//field[@name='month_3']"):
                node.set('string', month_3)
            for node in doc.xpath("//field[@name='month_4']"):
                node.set('string', month_4)
            for node in doc.xpath("//field[@name='month_5']"):
                node.set('string', month_5)
            for node in doc.xpath("//field[@name='month_6']"):
                node.set('string', month_6)
            for node in doc.xpath("//field[@name='month_7']"):
                node.set('string', month_7)
            for node in doc.xpath("//field[@name='month_8']"):
                node.set('string', month_8)
            for node in doc.xpath("//field[@name='month_9']"):
                node.set('string', month_9)
            for node in doc.xpath("//field[@name='month_10']"):
                node.set('string', month_10)
            for node in doc.xpath("//field[@name='month_11']"):
                node.set('string', month_11)
            for node in doc.xpath("//field[@name='month_12']"):
                node.set('string', month_12)
            res['arch'] = etree.tostring(doc, encoding='unicode')

        return res

    def get_month(self, num):
        today = datetime.now()
        print ('****')
        date = today + relativedelta(months=num)
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        return date.strftime('%b \'%y')

