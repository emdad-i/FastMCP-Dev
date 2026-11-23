from datetime import datetime
import platform
import time

from fastmcp import FastMCP
import psutil
from typing_extensions import TypedDict

mcp = FastMCP("Learning Server")


class CpuReport(TypedDict):
    logical_cores: int | None
    physical_cores: int | None
    usage_percent: float


class MemoryReport(TypedDict):
    total_gib: float
    used_gib: float
    available_gib: float
    usage_percent: float


class DiskReport(TypedDict):
    path: str
    total_gib: float
    used_gib: float
    available_gib: float
    usage_percent: float


class HardwareReport(TypedDict):
    measured_at: str
    platform: str
    architecture: str
    uptime_seconds: int
    cpu: CpuReport
    memory: MemoryReport
    disk: DiskReport


@mcp.tool
def add_numbers(first: int, second: int) -> int:
    """Add two whole numbers and return the result."""
    return first + second


@mcp.tool
def get_hardware_report(disk_path: str = ".") -> HardwareReport:
    """Report CPU, memory, uptime, and disk usage for this machine.

    System-wide CPU usage is sampled over half a second. Disk usage is measured
    for disk_path, which defaults to the current working directory's filesystem.
    """
    gib = 1024**3
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(disk_path)

    return {
        "measured_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "cpu": {
            "logical_cores": psutil.cpu_count(logical=True),
            "physical_cores": psutil.cpu_count(logical=False),
            "usage_percent": round(psutil.cpu_percent(interval=0.5), 1),
        },
        "memory": {
            "total_gib": round(memory.total / gib, 2),
            "used_gib": round(memory.used / gib, 2),
            "available_gib": round(memory.available / gib, 2),
            "usage_percent": memory.percent,
        },
        "disk": {
            "path": disk_path,
            "total_gib": round(disk.total / gib, 2),
            "used_gib": round(disk.used / gib, 2),
            "available_gib": round(disk.free / gib, 2),
            "usage_percent": disk.percent,
        },
    }


if __name__ == "__main__":
    mcp.run()
