import generate


def run():
    g = generate.generator()
    try:
        # g.export_batch()
        # g.export_batch_task()
        # g.export_task()
        g.export_data()
    finally:
        g.close()


if __name__ == '__main__':
    run()
