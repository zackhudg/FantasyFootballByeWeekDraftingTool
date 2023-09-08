import tkinter as tk
from tkinter import ttk
from simulation import simulate_draft, Team
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def create_gui(root):
    # Define a function to run simulations when the button is clicked
    def run_simulations_callback():
        league_size = int(league_size_var.get())
        league_scoring = scoring_var.get()
        draft_number = int(draft_number_var.get())
        num_rounds = int(num_rounds_var.get())
        adp_std = float(adp_std_var.get())
        number_of_sims = int(number_of_sims_var.get())

        # Simulate the draft and get a list of Team instances
        teams = simulate_draft(league_size, league_scoring, draft_number, num_rounds, adp_std, number_of_sims)

        # Create a subplot for the plot
        fig = make_subplots(rows=1, cols=1, subplot_titles=("Fantasy Football Draft Simulations"))
        
        # Create a scatter plot for the teams
        trace = go.Scatter(
            x=[team.bye_week for team in teams.keys()],
            y=[team.score for team in teams.keys()],
            text=[
                f"Draft Number: {team.draft_number}<br>"
                f"Bye Week: {team.bye_week}<br>"
                f"Score: {team.score}<br>"
                f"Diff Score: {team.diff_score}<br>"
                f"Frequency: {teams[team] / number_of_sims}<br>"
                "Team:<br>" + team.team_data[['Player', 'POS', 'AVG', 'MyPick', 'PickDiff']].to_string(max_colwidth=15, justify='right').replace("\n", "<br>")
            for team in teams.keys()],
            mode="markers",
            marker=dict(
                size=25, 
                color=[
                    f"rgba(255, 0, 0, {teams[team] / number_of_sims})"
                    for team in teams
                ],
            ),
        )

        # Add the trace to the subplot
        fig.add_trace(trace)

        # Customize the plot layout
        fig.update_xaxes(title_text="BYE Week")
        fig.update_yaxes(title_text="Score")
        fig.update_layout(
            showlegend=False,
            hovermode="closest",
            title_text="Fantasy Football Draft Simulations",
            xaxis=dict(
                title="BYE Week",
                tickvals=list(range(1, 17)),
                ticktext=[str(i) for i in range(1, 17)],
            ),
            yaxis=dict(title="Score"),
        )

        # Show the plot
        graph_div = go.Figure(fig)
        graph_div.update_xaxes(showline=True, linewidth=2, linecolor="black")
        graph_div.update_yaxes(showline=True, linewidth=2, linecolor="black")
        graph_div.show()

    # Create the main window
    root.title("Fantasy Football Draft Simulator")

    # Create an input frame for GUI components
    input_frame = ttk.Frame(root)
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Create a parameters frame for additional input options
    parameters_frame = ttk.Frame(input_frame)
    parameters_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Create a variable to toggle the display of parameters
    show_parameters = tk.BooleanVar(value=True)

    # Define a function to toggle the display of parameters
    def toggle_parameters():
        run_simulations_callback()

    # Create a checkbox to show/hide parameters
    toggle_checkbox = ttk.Checkbutton(parameters_frame, text="Show Parameters", variable=show_parameters, command=toggle_parameters)
    toggle_checkbox.grid(row=0, column=0, columnspan=3)

    # Create labels and entry fields for input parameters
    league_size_label = ttk.Label(parameters_frame, text="League Size:")
    league_size_label.grid(row=1, column=0, sticky="w")

    league_size_var = tk.StringVar(value="10")
    league_size_entry = ttk.Entry(parameters_frame, textvariable=league_size_var)
    league_size_entry.grid(row=1, column=1)

    scoring_var = tk.StringVar(value="HalfPPR")
    scoring_label = ttk.Label(parameters_frame, text="Scoring Format:")
    scoring_label.grid(row=2, column=0, sticky="w")

    ppr_radio = ttk.Radiobutton(parameters_frame, text="PPR", variable=scoring_var, value="PPR")
    ppr_radio.grid(row=2, column=1)

    halfppr_radio = ttk.Radiobutton(parameters_frame, text="HalfPPR", variable=scoring_var, value="HalfPPR")
    halfppr_radio.grid(row=2, column=2)

    std_radio = ttk.Radiobutton(parameters_frame, text="STD", variable=scoring_var, value="STD")
    std_radio.grid(row=2, column=3)

    draft_number_label = ttk.Label(parameters_frame, text="Draft Number:")
    draft_number_label.grid(row=3, column=0, sticky="w")

    draft_number_var = tk.StringVar(value="6")
    draft_number_entry = ttk.Entry(parameters_frame, textvariable=draft_number_var)
    draft_number_entry.grid(row=3, column=1)

    num_rounds_label = ttk.Label(parameters_frame, text="Number of Rounds:")
    num_rounds_label.grid(row=4, column=0, sticky="w")

    num_rounds_var = tk.StringVar(value="7")
    num_rounds_entry = ttk.Entry(parameters_frame, textvariable=num_rounds_var)
    num_rounds_entry.grid(row=4, column=1)

    adp_std_label = ttk.Label(parameters_frame, text="ADP_STD:")
    adp_std_label.grid(row=5, column=0, sticky="w")

    adp_std_var = tk.StringVar(value="0.02")
    adp_std_entry = ttk.Entry(parameters_frame, textvariable=adp_std_var)
    adp_std_entry.grid(row=5, column=1)
    
    number_of_sims_label = ttk.Label(parameters_frame, text="Number of Simulations:")
    number_of_sims_label.grid(row=6, column=0, sticky="w")

    number_of_sims_var = tk.StringVar(value="1")
    number_of_sims_entry = ttk.Entry(parameters_frame, textvariable=number_of_sims_var)
    number_of_sims_entry.grid(row=6, column=1)

    # Create a button to run simulations
    simulate_button = ttk.Button(parameters_frame, text="Simulate Drafts", command=run_simulations_callback)
    simulate_button.grid(row=7, column=0, columnspan=3)

    # Create a frame for the plot
    plot_frame = ttk.Frame(root)
    plot_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

if __name__ == "__main__":
    root = tk.Tk()
    create_gui(root)
    root.mainloop()
