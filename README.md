# campivargas07-branch-queue

## Branch Queue

Aplicación de terminal para gestionar tickets FIFO independientes por servicio.

### Ejemplo de comportamiento

Al emitir tickets alternando servicios, la numeración es global: Ana en `deposito` recibe el #1, Bruno en `retiro` el #2 y Carla en `deposito` el #3. Al llamar al siguiente de `deposito`, se atiende primero a Ana (#1) y Carla (#3) queda esperando. La cola de `retiro` permanece independiente.

El sistema implementa emisión, llamada y consulta del siguiente ticket, listado FIFO por servicio y estadísticas. Rechaza servicios inválidos y notifica cuando una cola está vacía; el CLI sigue funcionando tras entradas inválidas.

Ejecuta el menú con:

```bash
python3 branch_queue.py
```

Ejecuta las comprobaciones con:

```bash
python3 -m unittest -v test_branch_queue.py
```