from collections import deque
from dataclasses import dataclass
from datetime import datetime


SERVICES = ("deposito", "retiro", "gestion_cuenta")


@dataclass
class Ticket:
    number: int
    client_name: str
    service_type: str
    issued_at: datetime


class EmptyQueueError(Exception):
    """Raised when a service has no waiting tickets."""


class BranchQueue:
    def __init__(self):
        self._queues = {service: deque() for service in SERVICES}
        self._next_number = 1

    @staticmethod
    def _validate_service(service_type):
        if service_type not in SERVICES:
            valid = ", ".join(SERVICES)
            raise ValueError(f"Servicio inválido: {service_type!r}. Use uno de: {valid}.")

    def issue_ticket(self, client_name, service_type):
        self._validate_service(service_type)
        if not isinstance(client_name, str) or not client_name.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")

        ticket = Ticket(
            number=self._next_number,
            client_name=client_name.strip(),
            service_type=service_type,
            issued_at=datetime.now(),
        )
        self._next_number += 1
        self._queues[service_type].append(ticket)
        return ticket

    def call_next(self, service_type):
        self._validate_service(service_type)
        queue = self._queues[service_type]
        if not queue:
            raise EmptyQueueError(f"No hay clientes esperando para el servicio {service_type!r}.")
        # Concurrent callers must protect this check and removal as one operation.
        return queue.popleft()

    def peek_next(self, service_type):
        self._validate_service(service_type)
        queue = self._queues[service_type]
        if not queue:
            raise EmptyQueueError(f"No hay clientes esperando para el servicio {service_type!r}.")
        return queue[0]

    def list_waiting(self):
        return {service: list(queue) for service, queue in self._queues.items()}

    def stats(self):
        counts = {service: len(queue) for service, queue in self._queues.items()}
        counts["total"] = sum(counts.values())
        return counts


def _prompt_service():
    return input(f"Servicio ({'/'.join(SERVICES)}): ").strip()


def main():
    branch_queue = BranchQueue()
    menu = (
        "\nBranch Queue — Gestor de Cola por Servicio\n"
        "1. Emitir ticket\n"
        "2. Llamar al siguiente cliente\n"
        "3. Ver lista de espera\n"
        "4. Ver estadísticas\n"
        "5. Salir"
    )

    while True:
        print(menu)
        try:
            choice = input("Seleccione una opción: ").strip()
            if choice == "1":
                client_name = input("Nombre del cliente: ")
                service_type = _prompt_service()
                ticket = branch_queue.issue_ticket(client_name, service_type)
                print(
                    f"Ticket #{ticket.number} emitido para {ticket.client_name} "
                    f"({ticket.service_type}) a las {ticket.issued_at:%Y-%m-%d %H:%M:%S}."
                )
            elif choice == "2":
                service_type = _prompt_service()
                ticket = branch_queue.call_next(service_type)
                print(f"Siguiente: ticket #{ticket.number} — {ticket.client_name} ({ticket.service_type}).")
            elif choice == "3":
                waiting = branch_queue.list_waiting()
                for service, tickets in waiting.items():
                    print(f"{service}:")
                    if tickets:
                        for ticket in tickets:
                            print(f"  #{ticket.number} — {ticket.client_name} ({ticket.issued_at:%H:%M:%S})")
                    else:
                        print("  Sin clientes esperando.")
            elif choice == "4":
                for service, count in branch_queue.stats().items():
                    label = "Total" if service == "total" else service
                    print(f"{label}: {count}")
            elif choice == "5":
                print("Hasta luego.")
                return
            else:
                print("Opción inválida. Seleccione un número del 1 al 5.")
        except (ValueError, EmptyQueueError) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            return


if __name__ == "__main__":
    main()
