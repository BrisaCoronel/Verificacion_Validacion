# pylint: disable=C0114, C0116
import threading
import time
import struct
import os

# Constante para el nombre del archivo
FILENAME = "numeros_binarios.txt"

# Función para aplicar heapify
def heapyfy(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapyfy(arr, n, largest)

# Función para realizar heap sort
def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapyfy(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapyfy(arr, i, 0)

# Función para hacer el heap sort en paralelo
def parallel_heap_sort(arr, left, right, depth=0):
    max_depth = 9
    if depth >= max_depth:
        heap_sort(arr[left:right + 1])
    else:
        mid = left + (right - left) // 2
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]

        left_thread = threading.Thread(
        target=parallel_heap_sort,
        args=(left_arr, 0, len(left_arr) - 1, depth + 1)
)
        left_thread.start()
        parallel_heap_sort(right_arr, 0, len(right_arr) - 1, depth + 1)

        left_thread.join()

        i = j = 0
        k = left
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] < right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

# Función principal
def main():
    num_iterations = 1
    parallel_times = [0.0] * num_iterations
    serial_times = [0.0] * num_iterations

    # Secuencial
    for i in range(num_iterations):
        with open(FILENAME, "rb") as file:
            arr = list(struct.unpack("i" * (os.path.getsize(FILENAME) // 4), file.read()))

        start_serial = time.time()
        heap_sort(arr)
        end_serial = time.time()
        serial_times[i] = end_serial - start_serial

    # Paralelo
    for i in range(num_iterations):
        with open(FILENAME, "rb") as file:
            arr = list(struct.unpack("i" * (os.path.getsize(FILENAME) // 4), file.read()))

        start_parallel = time.time()
        parallel_heap_sort(arr, 0, len(arr) - 1)
        end_parallel = time.time()
        parallel_times[i] = end_parallel - start_parallel

    # Cálculo de tiempos
    total_parallel_time = sum(parallel_times)
    total_serial_time = sum(serial_times)

    average_parallel_time = total_parallel_time / num_iterations
    average_serial_time = total_serial_time / num_iterations
    speedup = average_serial_time / average_parallel_time
    efficiency = (speedup / (threading.active_count() / 2)) * 100

    print(f"Tiempo promedio en paralelo: {average_parallel_time:.6f} segundos")
    print(f"Tiempo promedio en serie: {average_serial_time:.6f} segundos")
    print(f"Speedup: {speedup:.6f}")
    print(f"Eficiencia: {efficiency:.6f}%")

if __name__ == "__main__":
    main()
