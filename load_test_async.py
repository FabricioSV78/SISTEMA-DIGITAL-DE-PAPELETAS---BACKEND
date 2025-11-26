"""
Simple async load test for the papeletas API.

Usage:
  pip install aiohttp tqdm
  python load_test_async.py --url http://127.0.0.1:8000 --concurrency 100 --total 1000 --auth "rrhh:12345678"

The script sends POST requests to /api/rrhh/crear-papeletas with random unique `codigo` values
so DB unique-constraint conflicts are unlikely unless you intentionally reuse codes.

Be careful: run this against staging or a test DB. Monitor DB and app resource usage.
"""

import asyncio
import aiohttp
import argparse
import random
import string
import uuid
from datetime import date, timedelta
from tqdm.asyncio import tqdm_asyncio

# Generate a random DNI-like string (8 digits)
def gen_dni():
    return ''.join(random.choices('0123456789', k=8))

# Generate a unique code
def gen_codigo():
    # nice readable code: PAPE-<uuid4 short>
    return 'PAPE-' + uuid.uuid4().hex[:12]

# Random date (past 2 years)
def gen_fecha():
    days_back = random.randint(0, 365 * 2)
    d = date.today() - timedelta(days=days_back)
    return d.isoformat()

# Payload template
def make_payload():
    nombre = random.choice(['Juan Pérez','María López','Carlos Sánchez','Ana Torres','Luis Gómez'])
    dni = gen_dni()
    codigo = gen_codigo()
    area = random.choice(['Finanzas','RRHH','Operaciones','Sistemas','Logística'])
    cargo = random.choice(['Analista','Coordinador','Asistente','Jefe'])
    motivo = random.choice(['Salida médica','Reunión externa','Gestiones','Capacitación'])
    oficina_entidad = random.choice(['Oficina Central','Sede Norte','Sede Sur'])
    fundamentacion = 'Prueba de carga - registro automático'
    fecha = gen_fecha()
    hora_salida = f"{random.randint(7,10):02d}:{random.choice([0,15,30,45]):02d}:00"
    hora_retorno = f"{random.randint(11,18):02d}:{random.choice([0,15,30,45]):02d}:00"
    regimen = random.choice(['CAS','PLANTA'])

    return {
        'nombre': nombre,
        'dni': dni,
        'codigo': codigo,
        'area': area,
        'cargo': cargo,
        'motivo': motivo,
        'oficina_entidad': oficina_entidad,
        'fundamentacion': fundamentacion,
        'fecha': fecha,
        'hora_salida': hora_salida,
        'hora_retorno': hora_retorno,
        'regimen': regimen
    }

async def worker(session, url, auth_header, semaphore, stats):
    async with semaphore:
        payload = make_payload()
        try:
            async with session.post(url + '/api/rrhh/crear-papeletas', json=payload, headers={'Authorization': f'Bearer {auth_header}', 'Content-Type': 'application/json'}) as resp:
                text = await resp.text()
                status = resp.status
                # update stats
                stats['total'] += 1
                if 200 <= status < 300:
                    stats['success'] += 1
                elif status == 409:
                    stats['conflict'] += 1
                elif status == 422:
                    stats['validation'] += 1
                else:
                    stats['errors'] += 1
                # optionally, store last message for debug
                if status >= 400 and stats['last_errors'] < 10:
                    stats['last_msgs'].append((status, text))
                    stats['last_errors'] += 1
        except Exception as e:
            stats['total'] += 1
            stats['errors'] += 1
            if stats['last_errors'] < 10:
                stats['last_msgs'].append(('exception', str(e)))
                stats['last_errors'] += 1

async def run(url, concurrency, total, auth):
    timeout = aiohttp.ClientTimeout(total=60)
    connector = aiohttp.TCPConnector(limit=0)
    semaphore = asyncio.Semaphore(concurrency)
    stats = {'total':0,'success':0,'conflict':0,'validation':0,'errors':0,'last_errors':0,'last_msgs':[]}
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = [worker(session, url, auth, semaphore, stats) for _ in range(total)]
        # Use tqdm to show progress
        for f in tqdm_asyncio.as_completed(tasks, total=total):
            await f

    print('\n--- Results ---')
    print(f"Total requests: {stats['total']}")
    print(f"Success:       {stats['success']}")
    print(f"Conflicts(409):{stats['conflict']}")
    print(f"Validations(422): {stats['validation']}")
    print(f"Other errors:   {stats['errors']}")
    if stats['last_msgs']:
        print('\nSample errors (up to 10):')
        for s,m in stats['last_msgs']:
            print(s, m)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:8000', help='Base URL of the API')
    parser.add_argument('--concurrency', type=int, default=50, help='Number of concurrent requests')
    parser.add_argument('--total', type=int, default=1000, help='Total number of requests to send')
    parser.add_argument('--auth', default='rrhh:12345678', help='Auth token content after Bearer (format usuario:dni)')
    args = parser.parse_args()

    print(f"Target: {args.url}/api/rrhh/crear-papeletas | concurrency={args.concurrency} | total={args.total}")

    asyncio.run(run(args.url, args.concurrency, args.total, args.auth))

if __name__ == '__main__':
    main()
