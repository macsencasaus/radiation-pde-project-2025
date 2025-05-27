#include <math.h>

extern unsigned int __heap_base;

__attribute__((import_module("jsExportObjects"),
               import_name("print"))) extern void
print(const char *str);

typedef unsigned char u8;
typedef int i32;
typedef unsigned u32;
typedef size_t usize;

u8 *bump_pointer = (u8 *)__heap_base;
__attribute__((export_name("malloc"))) 
void *malloc(u32 n) {
    void *p = (void *)bump_pointer;
    bump_pointer += n;
    return p;
}

__attribute((export_name("reset_malloc")))
void reset_malloc(void) {
    bump_pointer = (u8 *)__heap_base;
}

float *us;
u32 n_us;

struct input_data {
    u32 n_zones;
    u32 *n_cells;
    float *zone_length;
    float *sigma_t;
    float *source;
    float *boundary_values;
};

struct mesh {
    u32 n_points;
    u32 n_cells;
    float length;
    usize *cells;
    float *gridpoints;
    float *h;
    usize *mat_id;
};

input_data inp;
mesh m;

float *bs;

__attribute__((export_name("solve_transport")))
void solve_transport(float mu, u32 n_zones, u32 *n_cells, float *zone_length,
                     float *sigma_t, float *source, float *boundary_value) {
    for (u32 i = 0; i < n_zones; ++i) {
        m.n_cells += n_cells[i];
    }
    m.n_points = m.n_cells + 1;

    for (u32 i = 0; i < n_zones; ++i) {
        m.length += zone_length[i];
    }

    m.cells = (usize *)malloc(m.n_cells * sizeof(usize));
    for (u32 i = 0; i < m.n_cells; ++i) {
        m.cells[i] = i;
    }
    
    usize len = 0;
    for (u32 i = 0; i < n_zones; ++i) {
        len += n_cells[i];
    }

    m.h = (float *)malloc(len * sizeof(float));
    m.mat_id = (usize *)malloc(len * sizeof(usize));

    m.gridpoints = (float *)malloc((len + 1) * sizeof(float));
    m.gridpoints[0] = 0.f;

    for (u32 zone_idx = 0; zone_idx < n_zones; ++zone_idx) {
        float zone_len = zone_length[zone_idx];
        u32 zone_cells = n_cells[zone_idx];
        float dx = zone_len / zone_cells;

        for (u32 j = 0; j < zone_cells; ++j) {
            m.h[j] = dx;
            m.mat_id[j] = zone_idx;
            m.gridpoints[j + 1] = m.gridpoints[j] + dx;
        }
    }
}

void assemble_source(float mu) {
    bs = (float *)malloc(m.n_points * sizeof(float));
    for (int i = 1; i < m.n_points - 1; ++i) {
        float left_side = inp.source[m.mat_id[i - 1]] * m.h[i - 1];
        float right_side = inp.source[m.mat_id[i]] * m.h[i];
        bs[i] = (left_side * right_side) / 2;
    }

    if (mu < 0) {
        bs[0] = m.h[0] * inp.source[0] / 2;
        bs[m.n_points - 1] = inp.boundary_values[1];
    } else {
        bs[0] = inp.boundary_values[0];
        bs[m.n_points - 1] = m.h[m.n_points - 1] * inp.source[m.n_points - 1] / 2;
    }
}

// sparse matrix
float *rows, *cols, *data;

void generate_sparse_pattern(void) {
    rows = (float *)malloc(3 * m.n_points - 2);
    cols = (float *)malloc(3 * m.n_points - 2);
    usize rowsIdx = 0, colsIdx = 0;

    rows[rowsIdx] = rows[rowsIdx + 1] = 0;

    cols[colsIdx] = 0;
    cols[colsIdx + 1] = 1;

    colsIdx += 2;
    rowsIdx += 2;

    for (u32 i = 1; i < m.n_points - 1; ++i) {
        rows[rowsIdx + 0] = rows[rowsIdx + 1] = rows[rowsIdx + 2] = i;

        cols[colsIdx + 0] = i - 1;
        cols[colsIdx + 1] = i;
        cols[colsIdx + 2] = i + 1;

        colsIdx += 3;
        rowsIdx += 3;
    }

    u32 endIdx = m.n_points - 1;
    rows[rowsIdx + 0] = rows[rowsIdx + 1] = endIdx;

    cols[colsIdx + 0] = endIdx - 1;
    cols[colsIdx + 1] = endIdx;
}
