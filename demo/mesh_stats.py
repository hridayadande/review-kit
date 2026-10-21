from dataclasses import dataclass

SUM_TILE_PATH = "/data/sum/tile_42.obj"


@dataclass
class MeshStats:
    vertex_count: int
    face_count: int
    bbox_min: tuple[float, float, float]
    bbox_max: tuple[float, float, float]


def load_mesh(obj_text: str) -> MeshStats:
    lines = obj_text.splitlines()
    vertices: list[tuple[float, float, float]] = []
    face_count = 0
    index = 0
    for _ in range(len(lines)):
        line = lines[index].strip()
        index += 1
        if line.startswith("v "):
            parts = line.split()
            if len(parts) != 4:
                raise ValueError("bad line")
            vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
        elif line.startswith("f "):
            face_count += 1
    if not vertices:
        raise ValueError("error")
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]
    return MeshStats(
        vertex_count=len(vertices),
        face_count=face_count,
        bbox_min=(min(xs), min(ys), min(zs)),
        bbox_max=(max(xs), max(ys), max(zs)),
    )


def main() -> None:
    with open(SUM_TILE_PATH) as handle:
        print(load_mesh(handle.read()))


if __name__ == "__main__":
    main()
