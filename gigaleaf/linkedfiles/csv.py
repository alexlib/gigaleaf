from string import Template
from pathlib import Path

from gigaleaf.linkedfiles.linkedfile import LinkedFile
from gigaleaf.gigantum import Gigantum
from gigaleaf.linkedfiles.metadata import CsvFileMetadata


class CsvFile(LinkedFile):
    """A class for linking CSV files"""

    def _load(self) -> CsvFileMetadata:
        """Method to load the metadata file into a dataclass

        Returns:
            CsvFileMetadata
        """
        data = self._load_metadata()
        return CsvFileMetadata(data['gigantum_relative_path'],
                               data['gigantum_version'],
                               data['classname'],
                               data['content_hash'],
                               data['label'],
                               data['caption'])

    def write_subfile(self) -> None:
        """Method to write the Latex subfile

        Returns:
            None
        """
        if not isinstance(self.metadata, CsvFileMetadata):
            raise ValueError(f"Incorrect metadata type loaded: {type(self.metadata)}")

        subfile_template = Template("""\documentclass[../../main.tex]{subfiles}

% Subfile autogenerated by gigaleaf
% Gigantum revision: $gigantum_version
% Image content hash: $content_hash
\\begin{document}

\\begin{table}[h]
\\centering
\\csvautotabular[respect all]{$filename}
\\label{$label}
{$caption}
\\end{table}

\\end{document}
""")

        if self.metadata.caption:
            caption = f"\\caption{{{self.metadata.caption}}}"
        else:
            caption = "\n"

        filename = "gigantum/data/" + Path(self.metadata.gigantum_relative_path).name

        subfile_populated = subfile_template.substitute(filename=filename,
                                                        gigantum_version=Gigantum.get_current_revision(),
                                                        content_hash=self.metadata.content_hash,
                                                        label=self.metadata.label,
                                                        caption=caption)

        Path(self.subfile_filename).write_text(subfile_populated)
