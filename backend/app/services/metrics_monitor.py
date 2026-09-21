import time
import psutil
import subprocess
import threading
from app.services.windows_energy import create_energy_meter

class ProcessMonitor:

    def __init__(self, process):

        self.process = process

        self.cpu_samples = []
        self.memory_samples = []

        self.running = True
        self.total_cpu_time = 0.0
        self.max_memory_usage = 0.0
        self.monitor_start_time = None
        self.thread = threading.Thread(
            target=self._monitor,
            daemon=True
        )

    def start(self):
        self.thread.start()

    def stop(self):

        self.running = False

        if self.thread.is_alive():
            self.thread.join(timeout=2)

    def _monitor(self):

        try:

            ps_process = psutil.Process(
                self.process.pid
            )

            self.monitor_start_time = time.perf_counter()

            while self.running:

                total_cpu_time = 0.0
                total_memory = 0.0

                processes = []

                try:
                    processes.append(ps_process)

                    processes.extend(
                        ps_process.children(
                            recursive=True
                        )
                    )

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied
                ):
                    pass

                for proc in processes:

                    try:

                        cpu_times = proc.cpu_times()

                        total_cpu_time += (
                            cpu_times.user
                            + cpu_times.system
                        )

                        memory = (
                            proc.memory_info().rss
                            / (1024 * 1024)
                        )

                        total_memory += memory

                    except (
                        psutil.NoSuchProcess,
                        psutil.AccessDenied
                    ):
                        continue

                if total_cpu_time > self.total_cpu_time:
                    self.total_cpu_time = total_cpu_time
                if total_memory > self.max_memory_usage:
                    self.max_memory_usage = total_memory

                time.sleep(0.001)

        except Exception:
            pass

    def results(self, execution_time):

        if (
            execution_time > 0
            and self.total_cpu_time > 0
        ):
            cpu_usage = (
                self.total_cpu_time
                / execution_time
            ) * 100
        else:
            cpu_usage = 0.0

        return {
            "cpu_usage": float(cpu_usage),
            "memory_usage": float(
                self.max_memory_usage
            ),
        }

def execute_with_monitor(
    command,
    input_data,
    timeout=120
):

        energy_meter = None
        energy_before = None

        try:
            energy_meter = create_energy_meter(
                "RAPL_Package0_PKG"
            )

            energy_before = (
                energy_meter.read_package_energy()
            )

        except Exception:
            if energy_meter is not None:
                energy_meter.close()

            energy_meter = None
            energy_before = None

        start_time = time.perf_counter()

        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        monitor = ProcessMonitor(process)

        monitor.start()

        try:

            stdout, stderr = process.communicate(
                input=input_data,
                timeout=timeout
            )

        except subprocess.TimeoutExpired:

            process.kill()

            stdout, stderr = process.communicate()

            monitor.stop()
            if energy_meter is not None:
                energy_meter.close()

            raise TimeoutError(
                "Benchmark execution timed out."
            )
        
        energy_after = None

        if energy_meter is not None:

            try:

                energy_after = (
                    energy_meter.read_package_energy()
                )

            except Exception:

                energy_after = None

        monitor.stop()
        end_time = time.perf_counter()
        elapsed_seconds = (
            end_time - start_time
        )
        if process.returncode != 0:

            if energy_meter is not None:
                energy_meter.close()

            raise RuntimeError(
                f"Program execution failed:\n{stderr}"
            )

        metrics = monitor.results(
            elapsed_seconds
        )

        energy_joules = None

        if (
            energy_before is not None
            and energy_after is not None
        ):

            try:

                energy_joules = (
                    energy_meter.energy_delta_joules(
                        energy_before,
                        energy_after
                    )
                )

            except Exception:

                energy_joules = None

        
        if energy_meter is not None:
            energy_meter.close()

        execution_time = (
            end_time - start_time
        ) * 1000

        return {

            "stdout": stdout.strip(),

            "stderr": stderr.strip(),

            "execution_time": execution_time,

            "cpu_usage": metrics["cpu_usage"],

            "memory_usage": metrics[
                "memory_usage"
            ],
            "energy_consumption": energy_joules,
            
            "return_code": process.returncode,
        }


def measure_energy():

    """
    Placeholder for Intel RAPL.

    Returns None when RAPL is unavailable.

    Do NOT pretend that energy was measured.
    """

    return None