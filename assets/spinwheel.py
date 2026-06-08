class Wheel:
    @staticmethod
    def build_wheel(multipliers, pointer_index=None):
        display = [["", "", ""], ["", "🎡", ""], ["", "", ""]]

        positions = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]

        for i, (r, c) in enumerate(positions):
            value = f"{multipliers[i]}x"
            if pointer_index == i:
                display[r][c] = f"👉{value}👈"
            else:
                display[r][c] = value

        wheel_text = ""
        for row in display:
            wheel_text += "   ".join(row) + "\n"

        return f"```\n{wheel_text}\n```"
