# Part of OpenG2P Registry. See LICENSE file for full copyright and licensing details.
import logging

from odoo import fields, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class G2PMembershipGroup(models.Model):
    _inherit = "res.partner"

    group_membership_ids = fields.One2many(
        "g2p.group.membership", "group", "Group Members"
    )

    def count_individuals(self, relationship_kinds=None, domain=None):
        """
        Count the number of individuals in the group that match the kinds and domain.
        """
        _logger.info("SQL DEBUG: count_individuals: records:%s" % self.ids)
        membership_kind_domain = None
        individual_domain = None
        if self.group_membership_ids:
            if relationship_kinds:
                membership_kind_domain = [("name", "in", relationship_kinds)]
        else:
            return 0

        if domain is not None:
            individual_domain = domain

        query_result = self._query_members_aggregate(
            membership_kind_domain, individual_domain
        )

        return query_result

    def _query_members_aggregate(
        self, membership_kind_domain=None, individual_domain=None
    ):
        _logger.info("SQL DEBUG: query_members_aggregate: records:%s" % self.ids)
        ids = self.ids
        partner_model = "res.partner"
        domain = [("is_registrant", "=", True), ("is_group", "=", True)]
        query_obj = self.env[partner_model]._where_calc(domain)

        membership_alias = query_obj.left_join(
            "res_partner", "id", "g2p_group_membership", "group", "id"
        )
        individual_alias = query_obj.left_join(
            membership_alias, "individual", "res_partner", "id", "individual"
        )
        membership_kind_rel_alias = query_obj.left_join(
            membership_alias,
            "id",
            "g2p_group_membership_g2p_group_membership_kind_rel",
            "g2p_group_membership_id",
            "id",
        )
        rel_kind_alias = query_obj.left_join(
            membership_kind_rel_alias,
            "g2p_group_membership_kind_id",
            "g2p_group_membership_kind",
            "id",
            "id",
        )

        # Build where clause for the membership_alias
        membership_query_obj = expression.expression(
            model=self.env["g2p.group.membership"],
            domain=[("end_date", "=", None), ("group", "in", ids)],
            alias=membership_alias,
        ).query
        (
            membership_from_clause,
            membership_where_clause,
            membership_where_params,
        ) = membership_query_obj.get_sql()
        # _logger.info("SQL DEBUG: Membership Kind Query: From:%s, Where:%s, Params:%s" %
        #   (membership_from_clause,membership_where_clause,membership_where_params))
        query_obj.add_where(membership_where_clause, membership_where_params)

        if membership_kind_domain:
            membership_kind_query_obj = expression.expression(
                model=self.env["g2p.group.membership.kind"],
                domain=membership_kind_domain,
                alias=rel_kind_alias,
            ).query
            (
                membership_kind_from_clause,
                membership_kind_where_clause,
                membership_kind_where_params,
            ) = membership_kind_query_obj.get_sql()
            # _logger.info("SQL DEBUG: Membership Kind Query: From:%s, Where:%s, Params:%s" %
            #   (membership_kind_from_clause,membership_kind_where_clause,membership_kind_where_params))
            query_obj.add_where(
                membership_kind_where_clause, membership_kind_where_params
            )

        if individual_domain:
            individual_query_obj = expression.expression(
                model=self.env[partner_model],
                domain=individual_domain,
                alias=individual_alias,
            ).query
            (
                individual_from_clause,
                individual_where_clause,
                individual_where_params,
            ) = individual_query_obj.get_sql()
            # _logger.info("SQL DEBUG: Individual Query: From:%s, Where:%s, Params:%s" %
            #   (individual_from_clause,individual_where_clause,individual_where_params))
            query_obj.add_where(individual_where_clause, individual_where_params)

        select_query, select_params = query_obj.select(
            "res_partner.id AS id", "count(*) AS members_cnt"
        )

        # In the absence of managing "GROUP BY" by Odoo Query object,
        # we will add the GROUP BY clause manually
        select_query += " GROUP BY " + partner_model.replace(".", "_") + ".id"
        _logger.info(
            "SQL DEBUG: SQL query: %s, params: %s" % (select_query, select_params)
        )
        self._cr.execute(select_query, select_params)
        # Generate result as dict
        # results = self._cr.dictfetchall()
        # Generate result as tuple
        results = self._cr.fetchall()
        _logger.info("SQL DEBUG: SQL Query Result: %s" % results)
        return results

    def compute_count_and_set_indicator(
        self, field_name, kinds, domain, presence_only=False
    ):
        """
        This method is used to compute the count then set it.
        :param field_name: The Field Name.
        :param kinds: The Kinds.
        :param domain: The domain.
        :param presence_only: True for boolean field, False for integer field.
        :return: The count then set it on the Field Name.
        """

        _logger.info(
            "SQL DEBUG: compute_count_and_set_indicator: total records:%s" % len(self)
        )
        # Get groups only
        records = self.filtered(lambda a: a.is_group)
        query_result = None
        if records:
            # Generate the SQL query
            query_result = records.count_individuals(
                relationship_kinds=kinds, domain=domain
            )
            _logger.info(
                "SQL DEBUG: compute_count_and_set_indicator: field:%s, results:%s"
                % (field_name, query_result)
            )

            result_map = dict(query_result)
            for record in records:
                if presence_only:
                    record[field_name] = result_map.get(record.id, 0) > 0
                else:
                    record[field_name] = result_map.get(record.id, 0)

    def _update_compute_fields(
        self, records, field_name, kinds, domain, presence_only=False
    ):
        # Get groups only
        records = records.filtered(lambda a: a.is_group)

        query_result = None
        if records:
            # Generate the SQL query using Job Queue
            query_result = records.count_individuals(
                relationship_kinds=kinds, domain=domain
            )
            _logger.info(
                "SQL DEBUG: job_queue->_update_compute_fields: field:%s, results:%s"
                % (field_name, query_result)
            )
            # if query_result:
            #     # Update the compute fields and affected records

            result_map = dict(query_result)
            for record in records:
                _logger.info(
                    "SQL DEBUG: XXX job_queue->_update_compute_fields: record.id:%s, results:%s"
                    % (record.id, result_map.get(record.id, 0))
                )
                if presence_only:
                    record[field_name] = result_map.get(record.id, 0) > 0
                else:
                    record[field_name] = result_map.get(record.id, 0)
