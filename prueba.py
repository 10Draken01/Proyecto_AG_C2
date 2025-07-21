
layout = [
        [
            [
                [1, 0, 0],
                [0, 1, 0],
            ]
         , 1, 0],
        [1, 0, 1],
        [0, 0, 1]
]

def __Calculate_Celds(self):
        """
        Calcula el número de celdas ocupadas por las plantas.
        :return: Número de celdas ocupadas.
        """
        occupied_cells = 0
        for row in self.layout:
            for cell in row:
                if cell > 0: