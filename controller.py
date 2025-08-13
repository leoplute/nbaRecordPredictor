import json
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QObject, Signal

# This is a helper class to safely update the GUI from any thread,
# as I want to use the output area while the API fetches data, and then
# display the output when its ready
class ResultUpdater(QObject):
    update_result = Signal(str)
    update_error = Signal(str)
    enable_button = Signal()

class FantasyController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.executor = ThreadPoolExecutor(max_workers=1)
        
        # Create result updater for thread-safe GUI updates
        self.result_updater = ResultUpdater()
        self.result_updater.update_result.connect(lambda text: self.view.output_area.setText(text))
        self.result_updater.update_error.connect(lambda text: self.view.output_area.setText(text))
        self.result_updater.enable_button.connect(lambda: self.view.submit_btn.setEnabled(True))

        # Connect signals to slots
        self.view.submit_btn.clicked.connect(self.on_submit)
        self.view.output_area.setPlainText("Welcome to the lineup analyzer. Put in a starting 5 and submit to get an evaluation of the team")

    def on_submit(self):
        # Grab the inputted players, send them to be analyzed as a team
        pg = self.view.pginput.text()
        sg = self.view.sginput.text()
        sf = self.view.sfinput.text()
        pf = self.view.pfinput.text()
        c = self.view.cinput.text()

        if not pg or not sg or not sf or not pf or not c:
            self.view.output_area.setPlainText("Please have a player for every position")
            return

        players = [pg, sg, sf, pf, c]

        self.view.submit_btn.setEnabled(False)
        self.view.output_area.setPlainText('🏀 Analyzing your starting lineup...\n\n\n\n📊 Fetching player statistics...\n\n\n\n⏳ This may take a moment...')

        self.evaluate_lineup_async(players)


    # Nested function
    def evaluate_lineup_async(self, players):

        def on_complete(future):
            try:
                result = future.result()
                # Safely update GUI using signal
                self.result_updater.update_result.emit(result)
            except Exception as e:
                error_msg = f"Error analyzing lineup: {str(e)}"
                self.result_updater.update_error.emit(error_msg)
            finally:
                # Re-enable submit button 
                self.result_updater.enable_button.emit()

        # Start the evaluation in background
        future = self.executor.submit(self.model.evaluate_team, players)
        future.add_done_callback(on_complete)

    def cleanup(self):
        self.executor.shutdown(wait=True)