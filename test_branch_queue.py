import unittest

from branch_queue import BranchQueue, EmptyQueueError


class BranchQueueTests(unittest.TestCase):
    def setUp(self):
        self.queue = BranchQueue()

    def test_numbers_are_global_and_consecutive_across_services(self):
        first = self.queue.issue_ticket("Ana", "deposito")
        second = self.queue.issue_ticket("Beto", "retiro")
        third = self.queue.issue_ticket("Cora", "deposito")

        self.assertEqual([first.number, second.number, third.number], [1, 2, 3])

    def test_fifo_within_service_and_independence_between_services(self):
        deposito_first = self.queue.issue_ticket("Ana", "deposito")
        retiro_first = self.queue.issue_ticket("Beto", "retiro")
        deposito_second = self.queue.issue_ticket("Cora", "deposito")

        self.assertEqual(self.queue.call_next("deposito"), deposito_first)
        self.assertEqual(self.queue.call_next("deposito"), deposito_second)
        self.assertEqual(self.queue.peek_next("retiro"), retiro_first)
        self.assertEqual(self.queue.call_next("retiro"), retiro_first)

    def test_peek_does_not_remove_ticket(self):
        ticket = self.queue.issue_ticket("Ana", "gestion_cuenta")

        self.assertIs(self.queue.peek_next("gestion_cuenta"), ticket)
        self.assertEqual(self.queue.stats()["gestion_cuenta"], 1)
        self.assertIs(self.queue.call_next("gestion_cuenta"), ticket)

    def test_stats_count_services_and_total(self):
        self.queue.issue_ticket("Ana", "deposito")
        self.queue.issue_ticket("Beto", "retiro")
        self.queue.issue_ticket("Cora", "retiro")

        self.assertEqual(
            self.queue.stats(),
            {"deposito": 1, "retiro": 2, "gestion_cuenta": 0, "total": 3},
        )

    def test_list_waiting_groups_fifo_tickets_by_service(self):
        first = self.queue.issue_ticket("Ana", "retiro")
        self.queue.issue_ticket("Beto", "deposito")
        second = self.queue.issue_ticket("Cora", "retiro")

        waiting = self.queue.list_waiting()
        self.assertEqual(waiting["retiro"], [first, second])
        self.assertEqual(waiting["deposito"][0].client_name, "Beto")
        self.assertEqual(waiting["gestion_cuenta"], [])

    def test_empty_queue_raises_descriptive_error(self):
        with self.assertRaisesRegex(EmptyQueueError, "No hay clientes esperando"):
            self.queue.call_next("deposito")
        with self.assertRaisesRegex(EmptyQueueError, "No hay clientes esperando"):
            self.queue.peek_next("retiro")

    def test_invalid_service_is_rejected_without_consuming_ticket_number(self):
        with self.assertRaisesRegex(ValueError, "Servicio inválido"):
            self.queue.issue_ticket("Ana", "prestamo")
        with self.assertRaisesRegex(ValueError, "Servicio inválido"):
            self.queue.call_next("prestamo")
        with self.assertRaisesRegex(ValueError, "Servicio inválido"):
            self.queue.peek_next("prestamo")

        ticket = self.queue.issue_ticket("Beto", "deposito")
        self.assertEqual(ticket.number, 1)


if __name__ == "__main__":
    unittest.main()
