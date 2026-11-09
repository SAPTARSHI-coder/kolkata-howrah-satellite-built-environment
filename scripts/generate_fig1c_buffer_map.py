#!/Users/saptarshisadhu/miniconda3/envs/EDA/bin/python
"""
Generate publication-quality Figure 1c:
CAAQMS monitoring stations across Kolkata and Howrah with accurate 3 km radial
analysis buffers overlaid on high-resolution cartographic basemap.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def generate_fig1c():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    crop_path = "/Users/saptarshisadhu/Desktop/5_PAPERS/02_Paper_2_Atmospheric_Environment/figures/gis_layers/google_maps_kolkata_crop.png"
    out_path = os.path.join(base_dir, "figures", "fig1c_study_area_stations.png")
    
    if not os.path.exists(crop_path):
        raise FileNotFoundError(f"Basemap not found at {crop_path}")
        
    im = Image.open(crop_path)
    w_px, h_px = im.size

    # Projection parameters aligned with basemap crop
    crop_x0, crop_y0 = 850, 360
    lat0, lon0 = 22.6250807, 88.3629358
    z = 11.38
    W = 512.0 * (2.0 ** z)
    cx, cy = 1440.0, 1004.0

    def latlon_to_crop_pixel(lat, lon):
        x = cx + W * (lon - lon0) / 360.0
        l_rad = np.radians(lat)
        l0_rad = np.radians(lat0)
        y_m  = np.log(np.tan(np.pi / 4.0 + l_rad / 2.0))
        y_m0 = np.log(np.tan(np.pi / 4.0 + l0_rad / 2.0))
        y = cy - (W / (2.0 * np.pi)) * (y_m - y_m0)
        return x - crop_x0, y - crop_y0

    fig = plt.figure(figsize=(10.5, 11.5), dpi=300)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.imshow(im, extent=[0, w_px, h_px, 0])

    CATEGORIES = {
        'Heavy Industrial':      {'marker': 's', 'color': '#d63031', 'name': 'Heavy Industrial (DN, GH)'},
        'Commercial / Traffic':  {'marker': '^', 'color': '#0984e3', 'name': 'Commercial / Traffic (BN, RBU, JD)'},
        'Residential / Mixed':   {'marker': 'D', 'color': '#6c5ce7', 'name': 'Residential / Mixed (BG, BM, PP)'},
        'Background / Parkland': {'marker': 'o', 'color': '#00b894', 'name': 'Background / Parkland (BOG, FW, RS, SVSPA, VC)'},
    }

    STATIONS = {
        'DN':    {'name': 'Dasnagar',              'lat': 22.5960, 'lon': 88.3120, 'cat': 'Heavy Industrial'},
        'GH':    {'name': 'Ghusuri',               'lat': 22.6060, 'lon': 88.3510, 'cat': 'Heavy Industrial'},
        'BN':    {'name': 'Bidhannagar',           'lat': 22.5802, 'lon': 88.4331, 'cat': 'Commercial / Traffic'},
        'RBU':   {'name': 'Rabindra Bharati Univ', 'lat': 22.6268, 'lon': 88.3772, 'cat': 'Commercial / Traffic'},
        'JD':    {'name': 'Jadavpur',              'lat': 22.4991, 'lon': 88.3713, 'cat': 'Commercial / Traffic'},
        'BG':    {'name': 'Ballygunge',            'lat': 22.5264, 'lon': 88.3692, 'cat': 'Residential / Mixed'},
        'BM':    {'name': 'Belur Math',            'lat': 22.6362, 'lon': 88.3521, 'cat': 'Residential / Mixed'},
        'PP':    {'name': 'Padmapukur',            'lat': 22.5687, 'lon': 88.3118, 'cat': 'Residential / Mixed'},
        'BOG':   {'name': 'Botanical Garden',      'lat': 22.5585, 'lon': 88.2910, 'cat': 'Background / Parkland'},
        'FW':    {'name': 'Fort William',          'lat': 22.5532, 'lon': 88.3444, 'cat': 'Background / Parkland'},
        'VC':    {'name': 'Victoria Memorial',     'lat': 22.5441, 'lon': 88.3485, 'cat': 'Background / Parkland'},
        'RS':    {'name': 'Rabindra Sarovar',      'lat': 22.5083, 'lon': 88.3582, 'cat': 'Background / Parkland'},
        'SVSPA': {'name': 'Barrackpore',           'lat': 22.7661, 'lon': 88.3715, 'cat': 'Background / Parkland'},
    }

    # Custom label offsets
    OFFSETS = {
        'SVSPA': (-18,   0, 'right', 'center'),
        'BM':    (-18,  -6, 'right', 'center'),
        'RBU':   ( 18,   8, 'left',  'center'),
        'GH':    (-18,   6, 'right', 'center'),
        'DN':    (-18, -10, 'right', 'center'),
        'PP':    ( 18,  -4, 'left',  'center'),
        'BOG':   (-18,  -8, 'right', 'center'),
        'FW':    ( 18, -12, 'left',  'center'),
        'VC':    ( 18,  12, 'left',  'center'),
        'BN':    ( 18,   0, 'left',  'center'),
        'BG':    ( 18,   0, 'left',  'center'),
        'RS':    (-18,   0, 'right', 'center'),
        'JD':    ( 18,   0, 'left',  'center'),
    }

    # Buffer radius: 10 km = 370 px, so 3 km = 111.0 px
    BUFFER_RADIUS_PX = 111.0

    # 1. Draw 3 km radial buffer circles first (zorder=3)
    for code, st in STATIONS.items():
        cat = CATEGORIES[st['cat']]
        px, py = latlon_to_crop_pixel(st['lat'], st['lon'])
        
        # Transparent filled circle with styled boundary ring
        buffer_circle = patches.Circle(
            (px, py),
            radius=BUFFER_RADIUS_PX,
            facecolor=cat['color'],
            edgecolor=cat['color'],
            alpha=0.18,
            linewidth=1.8,
            linestyle='--',
            zorder=3
        )
        ax.add_patch(buffer_circle)
        
        # Solid subtle outer rim
        outer_ring = patches.Circle(
            (px, py),
            radius=BUFFER_RADIUS_PX,
            facecolor='none',
            edgecolor=cat['color'],
            alpha=0.75,
            linewidth=1.2,
            zorder=4
        )
        ax.add_patch(outer_ring)

    # 2. Draw station marker points (zorder=6) and labels (zorder=7)
    for code, st in STATIONS.items():
        cat = CATEGORIES[st['cat']]
        px, py = latlon_to_crop_pixel(st['lat'], st['lon'])
        
        # Station point marker
        ax.scatter(px, py, marker=cat['marker'], color=cat['color'],
                   s=130, edgecolors='black', linewidth=1.5, zorder=6)
        
        # Station callout label box
        dx, dy, ha, va = OFFSETS[code]
        ax.annotate(f"{st['name']} ({code})", xy=(px, py),
                    xytext=(px + dx, py + dy),
                    fontsize=8.5, fontweight='bold', ha=ha, va=va,
                    bbox=dict(boxstyle='round,pad=0.28', fc='white', ec=cat['color'], alpha=0.95, lw=1.3),
                    zorder=7)

    # Scale bar (10 km = 370 px)
    sb_box = patches.FancyBboxPatch((40, 1205), 440, 90, boxstyle="round,pad=6",
                                    fc='white', ec='#bdc3c7', alpha=0.94, lw=1.2, zorder=8)
    ax.add_patch(sb_box)
    sb_x, sb_y, sb_len = 75, 1255, 370
    ax.plot([sb_x, sb_x + sb_len], [sb_y, sb_y], color='black', lw=4, zorder=9)
    ax.plot([sb_x, sb_x + sb_len/2], [sb_y, sb_y], color='#2c3e50', lw=4, zorder=10)
    for x_tick in [sb_x, sb_x + sb_len/2, sb_x + sb_len]:
        ax.plot([x_tick, x_tick], [sb_y - 6, sb_y + 6], color='black', lw=2, zorder=9)
    ax.text(sb_x, sb_y - 12, '0', ha='center', fontsize=9.0, fontweight='bold', zorder=11)
    ax.text(sb_x + sb_len/2, sb_y - 12, '5', ha='center', fontsize=9.0, fontweight='bold', zorder=11)
    ax.text(sb_x + sb_len, sb_y - 12, '10 km', ha='center', fontsize=9.0, fontweight='bold', zorder=11)
    ax.text(sb_x + sb_len/2, sb_y + 19, 'Scale (Web Mercator) | Dashed Ring = 3 km Buffer',
            ha='center', fontsize=7.8, fontweight='semibold', color='#2c3e50', zorder=11)

    # North Arrow
    na_box = patches.FancyBboxPatch((55, 40), 80, 110, boxstyle="round,pad=6",
                                    fc='white', ec='#bdc3c7', alpha=0.94, lw=1.2, zorder=8)
    ax.add_patch(na_box)
    na_x, na_y = 95, 118
    ax.annotate('N', xy=(na_x, na_y - 45), xytext=(na_x, na_y),
                arrowprops=dict(facecolor='black', edgecolor='black', width=3.2, headwidth=11, headlength=15),
                ha='center', va='center', fontsize=14, fontweight='bold', zorder=9)

    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#d63031', markeredgecolor='k', markersize=9, label='Heavy Industrial (DN, GH)'),
        plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='#0984e3', markeredgecolor='k', markersize=9, label='Commercial / Traffic (BN, RBU, JD)'),
        plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#6c5ce7', markeredgecolor='k', markersize=8, label='Residential / Mixed (BG, BM, PP)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#00b894', markeredgecolor='k', markersize=9, label='Background / Parkland (BOG, FW, RS, SVSPA, VC)'),
        plt.Line2D([0], [0], linestyle='--', color='#2d3436', linewidth=1.8, label='3 km Landsat-8/9 Buffer ($28.3\\,\\text{km}^2$)'),
    ]
    leg = ax.legend(handles=legend_elements, loc='lower right', frameon=True, framealpha=0.96,
                    title='Land-Use Class & Buffer', title_fontsize=9.2,
                    prop={'size': 8.5})
    leg.get_frame().set_edgecolor('#bdc3c7')
    leg.set_zorder(10)

    # River Hooghly East/West Bank Annotations
    ax.text(280, 780, 'HOWRAH\n(West Bank)', fontsize=11, fontweight='bold', color='#2d3436',
            alpha=0.7, ha='center', va='center', zorder=5,
            bbox=dict(boxstyle='square,pad=0.3', fc='white', ec='none', alpha=0.5))
    ax.text(680, 840, 'KOLKATA\n(East Bank)', fontsize=11, fontweight='bold', color='#2d3436',
            alpha=0.7, ha='center', va='center', zorder=5,
            bbox=dict(boxstyle='square,pad=0.3', fc='white', ec='none', alpha=0.5))

    ax.set_xlim(0, w_px)
    ax.set_ylim(h_px, 0)
    ax.axis('off')

    plt.tight_layout(pad=0)
    fig.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"Successfully generated Figure 1c at: {out_path}")

if __name__ == "__main__":
    generate_fig1c()
