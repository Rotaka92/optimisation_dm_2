from distance import ManIsland


def get_distance_data():
    man_island = ManIsland()
    man_island.save_laposte_data()


if __name__ == "__main__":
    get_distance_data()