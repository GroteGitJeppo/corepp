"""
Optional PyTorch3D-accelerated geometry ops (FPS, ball query, kNN for FP).
Falls back to pure-PyTorch implementations in pointnet2_utils when unavailable.
No project-local .cu compilation — uses prebuilt pytorch3d wheels when installed.
"""
from __future__ import annotations

import torch

try:
    from pytorch3d.ops import ball_query, knn_points, sample_farthest_points

    _P3D_IMPORT_OK = True
except Exception:  # ImportError or missing CUDA extension at load time
    ball_query = None  # type: ignore[assignment]
    knn_points = None  # type: ignore[assignment]
    sample_farthest_points = None  # type: ignore[assignment]
    _P3D_IMPORT_OK = False


def pytorch3d_available() -> bool:
    return _P3D_IMPORT_OK


def _index_points(points: torch.Tensor, idx: torch.Tensor) -> torch.Tensor:
    """Gather points by batch indices [B, S, ...] from [B, N, C]."""
    device = points.device
    b = points.shape[0]
    view_shape = list(idx.shape)
    view_shape[1:] = [1] * (len(view_shape) - 1)
    repeat_shape = list(idx.shape)
    repeat_shape[0] = 1
    batch_indices = torch.arange(b, dtype=torch.long, device=device).view(view_shape).repeat(repeat_shape)
    return points[batch_indices, idx, :]


def farthest_point_sample_pytorch3d(xyz: torch.Tensor, npoint: int) -> torch.Tensor:
    """Returns [B, npoint] long indices. xyz: [B, N, 3]."""
    _, idx = sample_farthest_points(
        points=xyz,
        lengths=None,
        K=npoint,
        random_start_point=True,
    )
    return idx.long()


def query_ball_point_pytorch3d(
    radius: float,
    nsample: int,
    xyz: torch.Tensor,
    new_xyz: torch.Tensor,
) -> torch.Tensor:
    """
    new_xyz: query centers [B, S, 3], xyz: all points [B, N, 3].
    Returns [B, S, nsample] indices; duplicates closest-in-ball neighbor for padded slots (-1).
    """
    knn_res = ball_query(
        new_xyz,
        xyz,
        lengths1=None,
        lengths2=None,
        K=nsample,
        radius=radius,
        return_nn=False,
    )
    idx = knn_res.idx
    valid = idx >= 0
    row_has = valid.any(dim=-1)
    # First valid neighbor along K (PyTorch3D does not guarantee valid entries come first)
    first_mask = valid & (valid.cumsum(dim=-1) == 1)
    first = (first_mask.long() * idx).sum(dim=-1)
    first = torch.where(row_has, first, torch.zeros_like(first))
    pad = ~valid
    idx_out = idx.clone()
    fill = first.unsqueeze(-1).expand_as(idx)
    idx_out[pad] = fill[pad]
    return idx_out.long()


def feature_propagation_interpolate_pytorch3d(
    xyz1: torch.Tensor,
    xyz2: torch.Tensor,
    points2: torch.Tensor,
) -> torch.Tensor:
    """
    xyz1: [B, N, 3], xyz2: [B, S, 3], points2: [B, S, C]
    Returns interpolated [B, N, C] using inverse distance weights to 3 nearest in xyz2.
    """
    b, n, _ = xyz1.shape
    knn_res = knn_points(
        xyz1,
        xyz2,
        lengths1=None,
        lengths2=None,
        norm=2,
        K=3,
        return_nn=False,
        return_sorted=True,
    )
    dists = knn_res.dists
    idx = knn_res.idx
    dists = torch.clamp(dists, min=0.0)
    dist_recip = 1.0 / (dists + 1e-8)
    norm = torch.sum(dist_recip, dim=2, keepdim=True)
    weight = dist_recip / norm
    grouped = _index_points(points2, idx)
    return torch.sum(grouped * weight.view(b, n, 3, 1), dim=2)
