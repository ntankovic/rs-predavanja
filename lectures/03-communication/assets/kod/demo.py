"""Predavanje 03: gRPC demo usluge predaje (rok, nepoznat ishod, idempotentni ponovni pokušaj).

Pokretanje (Python 3.9+):
    pip install grpcio grpcio-tools
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. predaja.proto
    python demo.py

Poslužitelj i klijent rade u istom procesu radi jednostavnosti; poziv ipak ide preko gRPC-a i TCP-a.
"""
import sqlite3
import threading
import time
import uuid
from concurrent import futures

import grpc
import predaja_pb2
import predaja_pb2_grpc

baza = sqlite3.connect(":memory:", check_same_thread=False, isolation_level=None)
baza.execute("CREATE TABLE predaje (zapis_id TEXT PRIMARY KEY, predaja_id TEXT UNIQUE)")
brava = threading.Lock()
sporo_snimanje = {"ukljuceno": False}


class Predaja(predaja_pb2_grpc.PredajaServicer):
    def SnimiPredaju(self, zahtjev, context):
        with brava:
            # Ključ (predaja_id) i učinak (novi zapis) spremaju se jednom atomarnom naredbom.
            red = baza.execute(
                "INSERT INTO predaje (zapis_id, predaja_id) VALUES (?, ?) "
                "ON CONFLICT (predaja_id) DO NOTHING RETURNING zapis_id",
                (str(uuid.uuid4()), zahtjev.predaja_id)).fetchone()
            if red is None:  # ponovljeni pokušaj: vrati postojeći zapis
                zapis_id = baza.execute("SELECT zapis_id FROM predaje WHERE predaja_id = ?",
                                        (zahtjev.predaja_id,)).fetchone()[0]
                return predaja_pb2.OdgovorPredaje(zapis_id=zapis_id, vec_snimljeno=True)
            print(f"  [poslužitelj] snimljena predaja {zahtjev.predaja_id}")
        if sporo_snimanje["ukljuceno"]:
            time.sleep(3)  # predaja je snimljena, ali odgovor kasni
        return predaja_pb2.OdgovorPredaje(zapis_id=red[0])


def snimi(stub, predaja_id):
    zahtjev = predaja_pb2.ZahtjevPredaje(
        predaja_id=predaja_id, zadatak="RS-projekt", velicina_bajtova=20_971_520)
    try:
        odgovor = stub.SnimiPredaju(zahtjev, timeout=2.0)
        print(f"  [klijent] zapis {odgovor.zapis_id[:8]}, već snimljeno: {odgovor.vec_snimljeno}")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            print("  [klijent] DEADLINE_EXCEEDED: ishod nepoznat")
        else:
            raise


def main():
    posluzitelj = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    predaja_pb2_grpc.add_PredajaServicer_to_server(Predaja(), posluzitelj)
    posluzitelj.add_insecure_port("localhost:50051")
    posluzitelj.start()
    stub = predaja_pb2_grpc.PredajaStub(grpc.insecure_channel("localhost:50051"))

    print("1. Sporo snimanje, klijent čeka 2 s:")
    sporo_snimanje["ukljuceno"] = True
    snimi(stub, "p-2026-0812")
    sporo_snimanje["ukljuceno"] = False
    print("2. Ponovni pokušaj s istim predaja_id:")
    snimi(stub, "p-2026-0812")
    broj = baza.execute("SELECT COUNT(*) FROM predaje").fetchone()[0]
    print(f"Zapisa u tablici predaja: {broj}")
    posluzitelj.stop(0)


if __name__ == "__main__":
    main()
