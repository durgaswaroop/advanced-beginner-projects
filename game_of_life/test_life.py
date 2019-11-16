import pytest

from life import Universe
from life import render

class TestElementNextState:
    test_state = [
            #0,1,2,3,4,5,6,7,8,9
            [1,0,0,1,0,0,0,0,0,0], #0
            [0,0,0,1,0,0,0,1,0,0], #1
            [1,0,0,1,0,0,0,1,0,0], #2
            [1,1,0,0,0,0,0,1,0,0], #3
            [1,0,1,1,0,0,0,0,0,0], #4
            #0,1,2,3,4,5,6,7,8,9
            ]

    def setup(self):
        universe = Universe(size=5)
        universe.state = self.test_state
        return universe

    def test_input(self):
        """To ensure that the input is correct for the tests."""
        assert sum([sum(row) for row in self.test_state]) == 13

    # Live cell next generation tests
    def test_live_cell_with_fewer_than_two_live_neighbors_dies(self):
        universe = self.setup()
        # Live cell with 1 live neighbor
        assert universe.element_next_state(0,3) == 0 
        assert universe.element_next_state(2,3) == 0 
        assert universe.element_next_state(1,7) == 0
        assert universe.element_next_state(3,7) == 0

        # Live cell with 0 live neighbors
        assert universe.element_next_state(0,0) == 0

    def test_live_cell_with_two_or_three_live_neighbors_lives(self):
        universe = self.setup()
        # Live cell with two live neighbors
        assert universe.element_next_state(2,0) == 1 
        assert universe.element_next_state(4,0) == 1

        #Live cell with three live neighbors
        assert universe.element_next_state(3,0) == 1 

    def test_live_cell_with_more_than_three_live_neighbors_dies(self):
        universe = self.setup()
        assert universe.element_next_state(3,1) == 0
        assert universe.element_next_state(4,3) == 0

    # Dead cell next generation tests
    def test_dead_cell_with_three_live_neighbors_becomes_alive(self):
        universe = self.setup()
        assert universe.element_next_state(1,2) == 1
        assert universe.element_next_state(1,4) == 1
        assert universe.element_next_state(2,6) == 1
        assert universe.element_next_state(2,8) == 1

    def test_dead_cell_with_fewer_than_three_live_neighbors_stays_dead(self):
        universe = self.setup()
        # Dead cell with 2 live neighbors
        assert universe.element_next_state(1,0) == 0
        assert universe.element_next_state(2,4) == 0

        # Dead cell with 1 live neighbor
        assert universe.element_next_state(0,1) == 0
        assert universe.element_next_state(0,7) == 0

        # Dead cell with 0 live neighbors
        assert universe.element_next_state(0,9) == 0
        assert universe.element_next_state(4,9) == 0

    def test_dead_cell_with_more_than_three_live_neighbors_stays_dead(self):
        universe = self.setup()
        assert universe.element_next_state(4,1) == 0
        assert universe.element_next_state(4,7) == 0

class TestUniverseNextState:
    def test_glider_next_state(self):
        universe = Universe(size=5, configuration='glider')
        universe.next_state()

        expected_next_state = [
                #0,1,2,3,4,5,6,7,8,9
                [0,0,0,0,0,0,0,0,1,0], #0
                [0,0,0,0,0,0,1,1,0,0], #1
                [0,0,0,0,0,0,0,1,1,0], #2
                [0,0,0,0,0,0,0,0,0,0], #3
                [0,0,0,0,0,0,0,0,0,0], #4
                #0,1,2,3,4,5,6,7,8,9
                ]
        assert universe.state == expected_next_state

class TestRender:
    # TODO: Got to figure out how to test this
    @pytest.mark.xfail
    def test_render_output(self, capfd):
        universe = Universe(size=5, configuration='glider')
        # Prints the universe to console
        render(universe)

        out, err = capfd.readouterr()
        expected_out ="""
        ------------
        ı       ■  ı
        ı       ■ ■ı
        ı       ■■ ı
        ı          ı
        ı          ı
        ------------
        """.strip()
        assert out[:19] == expected_out[:19]
        # print(out[9:19])
        # print(expected_out[9:19])

        
