import json

class FantasyController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect signals to slots
        self.view.submit_btn.clicked.connect(self.on_submit)

    def on_submit(self):

        # Grab the inputted players, send them to be analyzed as a team
        pg = self.view.pginput.text()
        sg = self.view.sginput.text()
        sf = self.view.sfinput.text()
        pf = self.view.pfinput.text()
        c = self.view.cinput.text()
        players = [pg, sg, sf, pf, c]

        self.view.submit_btn.setEnabled(False)
        self.view.output_area.setPlainText('Loading...')

        output = self.model.evaluate_team(players)

        self.view.output_area.setText(output)
        #self.view.output_area.setText((json.dumps(output, indent=4)))
