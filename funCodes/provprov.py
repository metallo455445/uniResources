def norma(posizione):
    return np.linalg.norm(posizione)

def gradiente(X,Y):
    U = np.zeros_like(X, dtype=float)
    V = np.zeros_like(X, dtype=float)

    for p in particelle:
        massa = p.massa
        x0 = p.pos[0]
        y0 = p.pos[1]

        #distande del punto dalla massa
        dx = X - x0
        dy = Y - y0


        dist_quadro = dx**2 + dy**2

        dist_cubo = (dist_quadro + 1e-5)**(1.5)

        #somma componenti vettoriali
        U -= (constants.G * massa * dx) / dist_cubo 
        V -= (constants.G * massa * dy) / dist_cubo

    return (U, V)


p1 = particelle[0]
p2 = particelle[1]
cell = (1,1,1)
mesh = df.Mesh(p1=p1.pos, p2=p2.pos, cell=cell)
field = df.Field(mesh=mesh, nvdim=3, value=gradiente, norm=norma, valid='norm')
try:
    field.mpl()
except RuntimeError as e:
    print("Exception raised:", e)
