# Diseño

Cada servicio tiene su propia `collections.deque`. `call_next()` retira con `popleft()` en O(1), sin recorrer una lista compartida para localizar al primer cliente de ese servicio.

Si dos agentes del mismo servicio llamaran simultáneamente, la comprobación de cola no vacía y la extracción deben ser una sola operación protegida (por ejemplo, con un `threading.Lock` por servicio); de otro modo ambos podrían observar al mismo siguiente cliente. Esta aplicación no implementa concurrencia.
