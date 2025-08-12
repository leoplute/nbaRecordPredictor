import json

class FantasyController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect signals to slots
        self.view.submit_btn.clicked.connect(self.on_submit)

    def on_submit(self):
        players = [inp.text() for inp in self.view.inputs]

        self.view.submit_btn.setEnabled(False)
        self.view.output_area.setPlainText('Loading...')

        # Will want to switch this to evaluate team function
        output = self.model.evaluate_team(players)

        #self.view.output_area.setText(output)
        self.view.output_area.setText((json.dumps(output, indent=4)))
