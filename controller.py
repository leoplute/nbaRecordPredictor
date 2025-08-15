import json
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QObject, Signal, QTimer

# This is a helper class to safely update the GUI from any thread,
# as I want to use the output area while the API fetches data, and then
# display the output when its ready
class ResultUpdater(QObject):
    update_result = Signal(str)
    update_error = Signal(str)
    update_loading = Signal(str)
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
        self.result_updater.update_loading.connect(lambda text: self.view.output_area.setHtml(text))

        # Loading animation setup
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.update_loading_message)
        self.loading_messages = [
            '<div style="text-align: center; font-size: 24px; font-weight: bold;">🏀 Grabbing player stats...</div>',
            '<div style="text-align: center; font-size: 24px; font-weight: bold;">📊 Analyzing individual performances...</div>',
            '<div style="text-align: center; font-size: 24px; font-weight: bold;">🧠 Evaluating team chemistry...</div>',
            '<div style="text-align: center; font-size: 24px; font-weight: bold;">⚖️ Calculating synergies...</div>',
            '<div style="text-align: center; font-size: 24px; font-weight: bold;">🔮 Predicting team success...</div>',
            '<div style="text-align: center; font-size: 24px; font-weight: bold;">📈 Finishing up analysis...</div>',
            '<div style="text-align: center; font-size: 24px; font-weight: bold;">⏳ Almost there...</div>'
        ]
        self.loading_message_index = 0

        # Connect signals to slots
        self.view.submit_btn.clicked.connect(self.on_submit)
        self.view.output_area.setPlainText("Welcome to the lineup analyzer. Put in a starting 5 and submit to get an evaluation of the team")


    def update_loading_message(self):
        """Update the loading message to the next one in the cycle"""
        current_message = self.loading_messages[self.loading_message_index]
        self.result_updater.update_loading.emit(current_message)
        
        # Move to next message, cycle back to start if at end
        self.loading_message_index = (self.loading_message_index + 1) % len(self.loading_messages)

    def start_loading_animation(self):
        """Start the loading message animation"""
        self.loading_message_index = 0  
        self.update_loading_message() 
        self.loading_timer.start(1500)  

    def stop_loading_animation(self):
        """Stop the loading message animation"""
        self.loading_timer.stop()
        self.loading_message_index = 0  # Reset for next time

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

        self.start_loading_animation()

        self.evaluate_lineup_async(players)


    # Nested function
    def evaluate_lineup_async(self, players):

        def on_complete(future):
            try:
                self.stop_loading_animation()

                result = future.result()
                # Safely update GUI using signal
                self.result_updater.update_result.emit(result)
            except Exception as e:
                self.stop_loading_animation()
                error_msg = f"Error analyzing lineup: {str(e)}"
                self.result_updater.update_error.emit(error_msg)
            finally:
                # Re-enable submit button 
                self.result_updater.enable_button.emit()

        # Start the evaluation in background
        future = self.executor.submit(self.model.evaluate_team, players)
        future.add_done_callback(on_complete)

    def cleanup(self):
        self.loading_timer.stop()
        self.executor.shutdown(wait=True)